# -*- coding: utf-8 -*-

"""
Crawle boto3 documentation site, find all client id
"""

from typing import List

import re
import json
from diskcache import Cache
from pathlib_mate import Path

import requests
from bs4 import BeautifulSoup

# ------------------------------------------------------------------------------
dir_here = Path.dir_here(__file__)
dir_cache = Path(dir_here, ".cache")

cache = Cache(dir_cache.abspath)
cache_expire = 24 * 3600

path_service_id_list_json = Path(dir_here, "service_id_list.json")
# ------------------------------------------------------------------------------

def get_html_with_cache(url: str) -> str:
    if url in cache:
        return cache.get(url)
    else:
        html = requests.get(url).text
        cache.set(url, html, expire=cache_expire)
        return html


class ServiceHomepage:
    def __init__(self, name, url):
        self.name = name
        self.url = url


def get_all_service_homepage() -> List[ServiceHomepage]:
    """
    get all AWS Service boto3 api homepage
    """
    service_homepage_list = list()

    url_available_services = "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/index.html"
    html = get_html_with_cache(url_available_services)
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find("div", id="available-services")
    for a in div.find_all("a", class_="reference internal"):
        # make sure the link is a aws service link
        if "#" not in a.attrs["href"]:
            href_service_name = a.attrs["href"]
            name = a.text
            url = f"https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/{href_service_name}"
            service_homepage = ServiceHomepage(name=name, url=url)
            service_homepage_list.append(service_homepage)

    return service_homepage_list


def find_service_id_in_html(html: str):
    pattern = re.compile("client = boto3.client\('[\d\D]*'\)")
    soup = BeautifulSoup(html, "html.parser")
    div_client = soup.find("div", id="client")

    service_id = None
    for div_python in div_client.find_all("div", class_="highlight-python"):
        res = re.findall(pattern, div_python.text)
        if len(res):
            service_id = res[0].split("'")[1]
    return service_id


service_homepage_list = get_all_service_homepage()
service_id_list = list()
for service_homepage in service_homepage_list:
    print(f"working on {service_homepage.url} ...")
    html = get_html_with_cache(service_homepage.url)
    service_id = find_service_id_in_html(html)
    print(f"  {service_id}")
    service_id_list.append((service_homepage.name, service_id))
    # break
path_service_id_list_json.write_text(json.dumps(service_id_list))
