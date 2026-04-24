# -*- coding: utf-8 -*-

"""
Crawl `boto3 documentation site <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/index.html>`_,
find all client id and automatically generate code for this library.

Usage::

    python scripts/codegen/RUN_crawl_and_generate.py
"""

import typing as T
import json
import shutil
import dataclasses
from pathlib import Path

import jinja2
import httpx
from selectolax.parser import HTMLParser
from diskcache import Cache
from boto_session_manager.paths import path_enum

# ------------------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------------------
dir_here = Path(__file__).absolute().parent
dir_project_root = path_enum.dir_package
dir_cache = dir_here / ".cache"

path_spec_file_json = dir_here / "spec-file.json"
path_services_template = dir_here / "services.jinja2"
path_clients_template = dir_here / "clients.jinja2"
path_services_py = path_enum.dir_package / "services.py"
path_clients_py = path_enum.dir_package / "clients.py"

# ------------------------------------------------------------------------------
# Cache
# ------------------------------------------------------------------------------
cache = Cache(str(dir_cache))


def remove_cache():
    shutil.rmtree(dir_cache)


CACHE_EXPIRE = 24 * 3600  # 1 day

URL_SERVICES_INDEX = "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/index.html"


def get_html_with_cache(url: str) -> str:
    """
    Fetch URL content with disk-based caching (24h expiry).
    """
    if url in cache:
        return cache.get(url)
    html = httpx.get(url, follow_redirects=True).text
    cache.set(url, html, expire=CACHE_EXPIRE)
    return html


@dataclasses.dataclass
class AWSService:
    """
    Represents a single AWS service entry parsed from boto3 docs.

    :param name: sidebar display text, e.g. "EBS"
    :param href_name: filename part of the doc URL, e.g. "ebs.html"
    :param doc_url: full documentation URL
    :param service_id: boto3 client id, e.g. "ebs" for ``boto3.client("ebs")``
    """

    name: str
    href_name: str
    doc_url: str
    service_id: str = ""

    @property
    def name_snake_case(self) -> str:
        return self.name.lower().replace("-", "_")

    @property
    def service_id_snake_case(self) -> str:
        return self.service_id.lower().replace("-", "_")

    @property
    def service_id_camel_case(self) -> str:
        return "".join(
            word[0].upper() + word[1:] for word in self.name.lower().split("-")
        )


def parse_home_page(html: str) -> T.List[AWSService]:
    """
    Parse the boto3 services index page and return all AWS services.

    The service_id is derived from href_name by stripping the ``.html`` suffix,
    which matches the value used in ``boto3.client(service_id)``.
    This avoids crawling each individual service page.
    """
    aws_service_list: T.List[AWSService] = []
    tree = HTMLParser(html)
    ul = tree.css_first("ul.current")
    for a in ul.css("a.reference.internal"):
        href = a.attributes.get("href", "")
        if "#" in href:
            continue
        service_id = href.removesuffix(".html")
        aws_service_list.append(
            AWSService(
                name=a.text(),
                href_name=href,
                doc_url=f"https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/{href}",
                service_id=service_id,
            )
        )
    return aws_service_list


def get_all_aws_service() -> T.List[AWSService]:
    """
    Fetch the boto3 services index page and return all AWS services
    with name, href_name, doc_url, and service_id fully populated.
    """
    html = get_html_with_cache(URL_SERVICES_INDEX)
    return parse_home_page(html)


def step1_crawl_spec_file_data(limit: T.Optional[int] = None):
    """
    Crawl the boto3 docs index page, collect all service metadata,
    and write to spec-file.json.

    :param limit: if set, only process the first N services (for testing).
    """
    aws_service_list = get_all_aws_service()
    if limit is not None:
        aws_service_list = aws_service_list[:limit]
    print(f"Found {len(aws_service_list)} AWS services")

    spec_file_data = [dataclasses.asdict(svc) for svc in aws_service_list]
    path_spec_file_json.write_text(json.dumps(spec_file_data, indent=4))
    print(f"Wrote {path_spec_file_json}")


def step2_generate_code():
    """
    Read spec-file.json and render services.py and clients.py
    from Jinja2 templates.
    """
    spec_file_data = json.loads(path_spec_file_json.read_text())
    aws_service_list = [AWSService(**dct) for dct in spec_file_data]

    for path_template, path_output in [
        (path_services_template, path_services_py),
        (path_clients_template, path_clients_py),
    ]:
        rendered = jinja2.Template(path_template.read_text()).render(
            aws_service_list=aws_service_list,
        )
        path_output.write_text(rendered)
        print(f"Wrote {path_output}")


if __name__ == "__main__":
    step1_crawl_spec_file_data()
    step2_generate_code()
