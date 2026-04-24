
.. image:: https://readthedocs.org/projects/boto-session-manager/badge/?version=latest
    :target: https://boto-session-manager.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/boto_session_manager-project/actions/workflows/main.yml/badge.svg
    :target: https://github.com/MacHu-GWU/boto_session_manager-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/boto_session_manager-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/boto_session_manager-project

.. image:: https://img.shields.io/pypi/v/boto-session-manager.svg
    :target: https://pypi.python.org/pypi/boto-session-manager

.. image:: https://img.shields.io/pypi/l/boto-session-manager.svg
    :target: https://pypi.python.org/pypi/boto-session-manager

.. image:: https://img.shields.io/pypi/pyversions/boto-session-manager.svg
    :target: https://pypi.python.org/pypi/boto-session-manager

.. image:: https://img.shields.io/badge/✍️_Release_History!--None.svg?style=social&logo=github
    :target: https://github.com/MacHu-GWU/boto_session_manager-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/⭐_Star_me_on_GitHub!--None.svg?style=social&logo=github
    :target: https://github.com/MacHu-GWU/boto_session_manager-project

------

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://boto-session-manager.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/boto_session_manager-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/boto_session_manager-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/boto_session_manager-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/boto-session-manager#files


Welcome to ``boto_session_manager`` Documentation
==============================================================================
.. image:: https://boto-session-manager.readthedocs.io/en/latest/_static/boto_session_manager-logo.png
    :target: https://boto-session-manager.readthedocs.io/en/latest/

About ``boto_session_manager``
------------------------------------------------------------------------------
``boto_session_manager`` is a light weight, zero dependency python library that simplify managing your AWS boto3 session in your application code. It bring auto complete and type hint to the default ``boto3`` SDK, and provide smooth development experience with the following goodies:

- Create ``BotoSesManager`` from default credential, explicit credentials, named profiles, or a custom botocore session.
- 400+ typed client properties (e.g. ``bsm.s3_client``, ``bsm.ec2_client``) with IDE auto-complete and type hints powered by `boto3-stubs <https://pypi.org/project/boto3-stubs/>`_.
- Cached boto3 Client and Resource — each service client/resource is created once and reused.
- Assume IAM role — one-shot or auto-refreshable — and get a new ``BotoSesManager`` ready to go.
- Inspect your AWS identity: account ID, user ID, principal ARN, account alias, region, with optional masking for safe logging.
- ``awscli()`` context manager to temporarily inject credentials into ``os.environ`` for AWS CLI subprocesses.
- Credential snapshot: serialize credentials to a file and restore them in another process.
- Check session expiration and clear all internal caches when needed.

Additionally, if you use `boto3-stubs <https://pypi.org/project/boto3-stubs/>`_ and you did ``pip install "boto3-stubs[all]"``, then ``boto_session_manager`` comes with the auto complete and type hint for all boto3 methods out-of-the-box, without any extra configuration (such as `explicit type annotations <https://pypi.org/project/boto3-stubs/#explicit-type-annotations>`_)


Feature
------------------------------------------------------------------------------


Create a BotoSesManager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``BotoSesManager`` is the central entry point. It wraps a ``boto3.Session`` and provides caching, identity lookup, assume-role, and more. You can create one in several ways depending on how your AWS credentials are configured.

.. code-block:: python

    from boto_session_manager.api import BotoSesManager

    # 1. Use default credential chain (env vars, ~/.aws/credentials, instance profile, etc.)
    bsm = BotoSesManager()

    # 2. Use a named AWS profile from ~/.aws/credentials or ~/.aws/config
    bsm = BotoSesManager(profile_name="my_aws_profile")

    # 3. Use explicit credentials (e.g. from a secret store or CI/CD pipeline)
    bsm = BotoSesManager(
        aws_access_key_id="AKIA...",
        aws_secret_access_key="SECRET...",
        aws_session_token="TOKEN...",  # optional, for temporary credentials
        region_name="us-east-1",
    )

    # 4. Specify default kwargs that will be passed to every boto3 client
    #    e.g. always use a custom endpoint for local development with LocalStack
    bsm = BotoSesManager(
        default_client_kwargs={"endpoint_url": "http://localhost:4566"},
    )


Typed Client Properties with Auto-Complete
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``BotoSesManager`` exposes 400+ typed client properties — one for every AWS service. Simply type ``bsm.`` and your IDE will auto-complete the service name. Each property is a cached lazy accessor: the underlying ``boto3`` client is created on first access and reused afterward.

.. code-block:: python

    from boto_session_manager.api import BotoSesManager

    bsm = BotoSesManager()

    # Access the S3 client — fully typed, auto-completed by your IDE
    bsm.s3_client.list_buckets()  # returns {"Buckets": [...], ...}

    # Access the EC2 client
    bsm.ec2_client.describe_instances()

    # Access the Lambda client
    bsm.lambda_client.list_functions()

    # ... and 400+ more: bsm.dynamodb_client, bsm.sqs_client, bsm.iam_client, etc.

.. image:: https://github.com/MacHu-GWU/boto_session_manager-project/assets/6800411/c9f7f9bd-7b1d-4a3a-bacc-6296fd0c241a

One click to jump to the documentation:

.. image:: https://github.com/MacHu-GWU/boto_session_manager-project/assets/6800411/3d44c189-5900-4598-b493-47de97131793

Client method auto complete:

.. image:: https://github.com/MacHu-GWU/boto_session_manager-project/assets/6800411/c88ee956-b1ab-4d6c-aa3c-9df737ccd476

Arguments type hint:

.. image:: https://github.com/MacHu-GWU/boto_session_manager-project/assets/6800411/1978a8ed-ba21-4354-bde1-83e7652b4177

Note: you have to do ``pip install "boto3-stubs[all]"`` to enable "Client method auto complete" and "Arguments type hint" features.


Cached Client and Resource
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Every boto3 client and resource created through ``BotoSesManager`` is cached. Calling ``get_client()`` or ``get_resource()`` a second time for the same service returns the exact same object — no redundant connections, no wasted memory.

.. code-block:: python

    from boto_session_manager.api import BotoSesManager
    from boto_session_manager.api import AwsServiceEnum

    bsm = BotoSesManager()

    # --- Cached Client ---
    s3_client_1 = bsm.get_client(AwsServiceEnum.S3)
    s3_client_2 = bsm.get_client(AwsServiceEnum.S3)
    assert id(s3_client_1) == id(s3_client_2)  # same object, pulled from cache

    # The typed property shortcut also uses the same cache:
    s3_client_3 = bsm.s3_client
    assert id(s3_client_1) == id(s3_client_3)

    # --- Cached Resource ---
    s3_resource_1 = bsm.get_resource(AwsServiceEnum.S3)
    s3_resource_2 = bsm.get_resource(AwsServiceEnum.S3)
    assert id(s3_resource_1) == id(s3_resource_2)  # also cached


AWS Identity Inspection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``BotoSesManager`` provides convenient cached properties to query your current AWS identity via STS ``GetCallerIdentity`` and IAM ``ListAccountAliases``. Each property is resolved lazily on first access and cached afterward.

For safe logging, every identity property has a masked counterpart that redacts sensitive digits.

.. code-block:: python

    from boto_session_manager.api import BotoSesManager

    bsm = BotoSesManager()

    # --- Account and identity info (cached, calls STS once) ---
    bsm.aws_account_id          # "123456789012"
    bsm.aws_account_user_id     # "AIDA..."
    bsm.principal_arn            # "arn:aws:iam::123456789012:user/my-user"
    bsm.aws_region               # "us-east-1"
    bsm.aws_account_alias        # "my-account-alias" or None

    # --- Masked versions for safe logging ---
    bsm.masked_aws_account_id          # "12**********12"
    bsm.masked_aws_account_user_id     # "AI**...DA"
    bsm.masked_principal_arn            # "arn:aws:iam::12**********12:user/my-user"

    # --- Print a human-friendly summary ---
    bsm.print_who_am_i()
    # User Id = AI**...DA
    # AWS Account Id = 12**********12
    # Principal Arn = arn:aws:iam::12**********12:user/my-user
    # AWS Account Alias = my-account-alias
    # AWS Region = us-east-1

    # Pass masked=False to see unredacted values
    bsm.print_who_am_i(masked=False)


Assume IAM Role
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Call ``assume_role()`` to get a brand-new ``BotoSesManager`` that operates under a different IAM role. The returned object is a fully independent session with its own caches.

.. code-block:: python

    from boto_session_manager.api import BotoSesManager

    bsm = BotoSesManager()

    # Assume a role and get a new session manager
    bsm_assumed = bsm.assume_role(
        role_arn="arn:aws:iam::111122223333:role/my-role",
        duration_seconds=3600,  # default: 1 hour
    )

    # The assumed session is a full BotoSesManager — all features work
    bsm_assumed.sts_client.get_caller_identity()
    # {"Account": "111122223333", "Arn": "arn:aws:sts::111122223333:assumed-role/my-role/..."}

    # You can also pass optional parameters
    bsm_assumed = bsm.assume_role(
        role_arn="arn:aws:iam::111122223333:role/my-role",
        role_session_name="my-session",
        tags=[{"Key": "Project", "Value": "demo"}],
        external_id="my-external-id",
        region_name="eu-west-1",  # switch region at the same time
    )


Auto-Refreshable Assumed Role
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For long-running processes, pass ``auto_refresh=True`` so the assumed-role credentials are transparently refreshed before they expire. This uses ``botocore``'s internal ``DeferredRefreshableCredentials`` mechanism.

.. code-block:: python

    import time
    from boto_session_manager.api import BotoSesManager

    bsm = BotoSesManager()

    bsm_assumed = bsm.assume_role(
        role_arn="arn:aws:iam::111122223333:role/my-role",
        duration_seconds=900,   # 15-minute tokens
        auto_refresh=True,      # botocore will refresh them automatically
    )

    # Even though each token lives only 15 minutes,
    # the session keeps working for as long as the source credentials are valid.
    for i in range(60):
        time.sleep(60)
        # This call will succeed even after 15 minutes — credentials refresh automatically
        print(bsm_assumed.sts_client.get_caller_identity()["Account"])

.. note::

    ``auto_refresh`` relies on ``AssumeRoleCredentialFetcher`` and ``DeferredRefreshableCredentials`` from botocore, which are not public API officially supported by botocore. This API may be unstable.


Check Session Expiration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you obtain credentials from ``assume_role()`` (without ``auto_refresh``), they have a finite lifetime. Use ``is_expired()`` to check whether the session is still valid, optionally with a safety margin.

.. code-block:: python

    from boto_session_manager.api import BotoSesManager

    bsm = BotoSesManager()
    bsm_assumed = bsm.assume_role(
        role_arn="arn:aws:iam::111122223333:role/my-role",
        duration_seconds=3600,
    )

    bsm_assumed.is_expired()       # False (just created)

    # Check if it will expire within the next 5 minutes (300 seconds)
    # Useful for proactively refreshing before a long operation
    bsm_assumed.is_expired(delta=300)  # True if less than 5 min remaining


AWS CLI Context Manager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``awscli()`` context manager temporarily injects the session's credentials into ``os.environ`` so that any AWS CLI subprocess (or tool that reads environment variables) uses the same identity. On exit, the original environment is restored.

.. code-block:: python

    import os
    import subprocess
    from boto_session_manager.api import BotoSesManager

    bsm = BotoSesManager(profile_name="my_aws_profile")

    # Before: env vars are not set
    os.environ.get("AWS_ACCESS_KEY_ID")  # None

    with bsm.awscli():
        # Inside: env vars are set to bsm's credentials
        os.environ.get("AWS_ACCESS_KEY_ID")   # "AKIA..."
        os.environ.get("AWS_SECRET_ACCESS_KEY")  # "SECRET..."
        os.environ.get("AWS_REGION")          # "us-east-1"

        # Any subprocess now uses the same identity
        subprocess.run(["aws", "sts", "get-caller-identity"])

    # After: env vars are restored to their original state
    os.environ.get("AWS_ACCESS_KEY_ID")  # None (back to original)

This also works with assumed-role sessions:

.. code-block:: python

    bsm_assumed = bsm.assume_role(
        role_arn="arn:aws:iam::111122223333:role/my-role",
    )

    with bsm_assumed.awscli():
        # AWS CLI now operates under the assumed role
        # AWS_SESSION_TOKEN is also set automatically
        subprocess.run(["aws", "s3", "ls"])


Credential Snapshot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes you need to pass credentials across process boundaries — for example, when a parent script assumes a role and launches a child script that needs the original (pre-assume) credentials. The snapshot mechanism serializes credentials to a JSON file and lets another process restore them.

.. code-block:: python

    import subprocess
    from boto_session_manager.api import BotoSesManager

    bsm = BotoSesManager()

    # --- Serialize to dict ---
    snapshot = bsm.to_snapshot()
    # {"region_name": "us-east-1", "aws_access_key_id": "AKIA...", "aws_secret_access_key": "..."}

    # --- Restore from dict ---
    bsm_restored = BotoSesManager.from_snapshot(snapshot)
    bsm_restored.aws_account_id  # same as original

    # --- temp_snapshot() context manager ---
    # Writes credentials to ~/.bsm-snapshot.json, then deletes the file on exit.
    bsm_default = BotoSesManager()
    bsm_other = BotoSesManager(profile_name="other_account")

    with bsm_default.temp_snapshot():
        with bsm_other.awscli():
            # env now points to "other_account"
            # but child processes can recover the original session:
            # inside my_child_script.py:
            #     bsm_origin = BotoSesManager.from_snapshot_file()
            subprocess.run(["python", "my_child_script.py"])

    # ~/.bsm-snapshot.json is automatically deleted here

    # --- Restore from file (used in child processes) ---
    bsm_origin = BotoSesManager.from_snapshot_file()  # reads ~/.bsm-snapshot.json
    bsm_origin = BotoSesManager.from_snapshot_file("/path/to/custom-snapshot.json")


Clear Cache
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``clear_cache()`` resets all internal caches — the underlying boto3 session, all service clients and resources, and the cached identity properties. This is useful when credentials have changed or when you want to force fresh connections.

.. code-block:: python

    from boto_session_manager.api import BotoSesManager

    bsm = BotoSesManager()

    # Use some clients — they get cached
    bsm.s3_client.list_buckets()
    bsm.ec2_client.describe_instances()
    _ = bsm.aws_account_id  # cached STS call

    # Clear everything — next access will create fresh clients
    bsm.clear_cache()

    # These will create new boto3 clients from scratch
    bsm.s3_client.list_buckets()


.. _install:

Install
------------------------------------------------------------------------------

``boto_session_manager`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install boto_session_manager

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade boto_session_manager
