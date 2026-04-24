.. _Integration-Test-Strategy:

Integration Test Strategy
==============================================================================

Overview
------------------------------------------------------------------------------
This project tests against a **real AWS account** — no mocks, no LocalStack.
A dedicated IAM User and IAM Role are provisioned with minimal permissions
using AWS CDK. The test suite authenticates with real credentials and exercises
actual STS / IAM API calls, giving us confidence that the library works
end-to-end with AWS.

The overall flow:

1. **CDK** creates the IAM User and Role (infrastructure).
2. **Python scripts** create an access key for the User and write it to a
   local ``.env`` file (credentials never touch CloudFormation).
3. **Another script** uploads the same credentials to GitHub Actions secrets
   so CI can authenticate.
4. **pytest** reads the credentials (from env vars in CI, from ``.env``
   locally) and runs integration tests.


Constants
------------------------------------------------------------------------------
All test-related constants (IAM user/role names, GitHub secret names) live in
a single file so that CDK, access-key scripts, CI config, and test code all
reference the same values:

.. literalinclude:: ../../../../boto_session_manager/tests/settings.py
   :language: python


IAM Infrastructure (CDK)
------------------------------------------------------------------------------
The CDK stack lives in the ``cdk/`` directory. It creates:

- **IAM User** — program-only access, with an inline policy that allows
  ``sts:AssumeRole`` (scoped to the test role), ``sts:GetCallerIdentity``,
  ``sts:GetAccessKeyInfo``, and ``iam:ListAccountAliases``.
- **IAM Role** — trusted by the account root principal, with the same
  STS / IAM read permissions. Tests use ``assume_role()`` to switch into
  this role.

The CDK stack does **not** manage access keys — those are created separately
(see next section) so that the secret key never gets persisted in
CloudFormation state.

The AWS profile used for CDK operations is defined in ``mise.toml``:

.. literalinclude:: ../../../../mise.toml
   :language: toml
   :lines: 1-5

The CDK app:

.. literalinclude:: ../../../../cdk/app.py
   :language: python


Access Key Management
------------------------------------------------------------------------------
Access keys are managed by Python scripts using boto3, **not** by CDK. This
ensures the secret key only ever appears in the ``create-access-key`` API
response and is written directly to the local ``.env`` file — it never gets
stored in CloudFormation outputs or state.

The core logic lives in ``cdk/iam_access_key.py``:

.. literalinclude:: ../../../../cdk/iam_access_key.py
   :language: python

Two thin entry-point scripts import and call the functions above:

**Create** — deletes any existing keys, creates a fresh one, writes ``.env``:

.. literalinclude:: ../../../../cdk/create_access_key.py
   :language: python

**Delete** — removes all keys and deletes ``.env``:

.. literalinclude:: ../../../../cdk/delete_access_key.py
   :language: python


GitHub Actions Secrets
------------------------------------------------------------------------------
After the access key is written to ``.env``, a separate script reads it and
uploads the credentials to GitHub Actions secrets using the PyGithub library.
This is how CI gets the credentials without checking them into the repo.

.. literalinclude:: ../../../../.mise/tasks/setup_github_action_secret.py
   :language: python

The CI workflow references these secrets in ``.github/workflows/main.yml``:

.. literalinclude:: ../../../../.github/workflows/main.yml
   :language: yaml
   :lines: 76-83
   :emphasize-lines: 4-5


mise Tasks — Putting It All Together
------------------------------------------------------------------------------
The ``mise.toml`` file defines two tasks that orchestrate the full lifecycle:

**cdk-up** — deploy infrastructure, create access key, push secrets to GitHub:

.. literalinclude:: ../../../../mise.toml
   :language: toml
   :lines: 126-134

**cdk-down** — delete access key and ``.env``, then destroy the CDK stack:

.. literalinclude:: ../../../../mise.toml
   :language: toml
   :lines: 136-142

Typical usage:

.. code-block:: bash

    # first time setup (or after rotating credentials)
    mise run cdk-up

    # run tests locally
    mise run cov

    # tear everything down
    mise run cdk-down


Test Code
------------------------------------------------------------------------------
The test file ``tests/test_manager.py`` handles both local and CI
environments. It detects the ``CI`` environment variable to decide where
to read credentials from:

- **CI**: reads from GitHub Actions secrets (injected as env vars).
- **Local**: uses ``python-dotenv`` to load from the ``.env`` file created
  by ``create_access_key.py``.

.. literalinclude:: ../../../../tests/test_manager.py
   :language: python
   :lines: 1-43
   :caption: tests/test_manager.py (credential setup)
