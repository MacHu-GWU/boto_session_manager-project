Code Generation
==============================================================================

Overview
------------------------------------------------------------------------------
This project does **not** hand-write the 400+ AWS service enum values or their corresponding typed client properties. Instead, a code-generation script crawls the official `boto3 documentation <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/index.html>`_, collects every service name and client ID into a spec file, and then renders Python source files from Jinja2 templates.

Whenever AWS releases new services, re-running the script brings everything up to date automatically.


How It Works
------------------------------------------------------------------------------
The entire pipeline lives in ``scripts/codegen/`` and consists of two steps:

**Step 1 — Crawl** (``step1_crawl_spec_file_data``):

1. Fetches the boto3 services index page.
2. Parses the sidebar to extract every service's display name, href, documentation URL, and client ID (the string you pass to ``boto3.client(...)``).
3. Writes the result to ``scripts/codegen/spec-file.json``.

HTTP responses are cached on disk (in ``scripts/codegen/.cache/``, git-ignored) with a 24-hour expiry, so repeated runs during development don't hammer the boto3 docs site.

**Step 2 — Generate** (``step2_generate_code``):

1. Reads ``spec-file.json``.
2. Renders two Jinja2 templates against the service list:

   - ``services.jinja2`` → ``boto_session_manager/services.py`` — the ``AwsServiceEnum`` class with one class attribute per service (e.g. ``AccessAnalyzer = "accessanalyzer"``).
   - ``clients.jinja2`` → ``boto_session_manager/clients.py`` — the ``ClientMixin`` class with one ``@property`` per service (e.g. ``bsm.accessanalyzer_client``) that returns a typed boto3 client, leveraging ``mypy-boto3-*`` stubs for IDE autocomplete.

Both steps run in sequence when you execute::

    python scripts/codegen/RUN_crawl_and_generate.py


File Layout
------------------------------------------------------------------------------
::

    scripts/codegen/
    ├── RUN_crawl_and_generate.py   # entry point — run this to regenerate
    ├── services.jinja2             # template for AwsServiceEnum
    ├── clients.jinja2              # template for ClientMixin
    ├── spec-file.json              # crawled service metadata (checked in)
    ├── .cache/                     # HTTP response cache (git-ignored)
    └── .gitignore                  # ignores .cache/


Key Data Model
------------------------------------------------------------------------------
Each AWS service is represented by the ``AWSService`` dataclass with these fields:

- ``name`` — sidebar display text (e.g. ``"EBS"``), used as the enum attribute name.
- ``href_name`` — filename from the doc URL (e.g. ``"ebs.html"``).
- ``doc_url`` — full boto3 documentation URL.
- ``service_id`` — the string passed to ``boto3.client(service_id)`` (e.g. ``"ebs"``), derived from ``href_name`` by stripping the ``.html`` suffix.

Derived properties convert the name to ``snake_case`` (for Python identifiers) and ``CamelCase`` as needed by the templates.


When to Re-run
------------------------------------------------------------------------------
Re-run the code generation script when:

- **AWS launches new services** — the new service will appear on the boto3 docs index page.
- **A service is renamed or removed** — the spec file and generated code will update accordingly.
- **You modify a Jinja2 template** — e.g. to change the generated property signature or add new functionality.

After re-running, review the diff in ``services.py`` and ``clients.py`` to confirm the changes look correct before committing.


Dependencies
------------------------------------------------------------------------------
The code generation script requires several packages beyond the project's runtime dependencies:

- `jinja2 <https://jinja.palletsprojects.com>`_ — template rendering
- `httpx <https://www.python-httpx.org>`_ — HTTP client for fetching boto3 docs
- `selectolax <https://github.com/rushter/selectolax>`_ — fast HTML parsing
- `diskcache <https://grantjenks.com/docs/diskcache/>`_ — disk-based HTTP response caching

These are development-only dependencies and are not required at runtime.
