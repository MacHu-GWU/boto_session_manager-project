# -*- coding: utf-8 -*-

"""
Upload IAM access key credentials from .env to GitHub Actions secrets.

Reads ``AWS_ACCESS_KEY_ID`` and ``AWS_SECRET_ACCESS_KEY`` from ``.env``,
then creates/updates the corresponding GitHub Actions secrets:

- ``AWS_ACCESS_KEY_ID_FOR_GITHUB_CI``
- ``AWS_SECRET_ACCESS_KEY_FOR_GITHUB_CI``

Required environment variables (set by mise.toml):
- GITHUB_TOKEN: GitHub personal access token with repo scope

Usage: python cdk/setup_github_action_secret.py
"""

import os
import sys
from pathlib import Path

try:
    from github import Github, GithubException, Auth
except ImportError:
    print("Error: PyGithub not installed. Run: uv sync --extra mise")
    sys.exit(1)

# fmt: off
from boto_session_manager.tests.settings import GITHUB_ENV_VAR_NAME_FOR_AWS_ACCESS_KEY_ID_FOR_GITHUB_CI
from boto_session_manager.tests.settings import GITHUB_ENV_VAR_NAME_FOR_AWS_SECRET_ACCESS_KEY_FOR_GITHUB_CI
# fmt: on

# reuse the project-level utility to discover owner/repo from git remote
sys.path.insert(0, str(Path(__file__).parent.parent / ".mise" / "tasks"))
from utils import get_github_repo_info

ENV_FILE = Path(__file__).parent.parent.parent / ".env"  # MAKE SURE THIS IS RIGHT


# mapping: .env key -> GitHub Actions secret name
SECRET_MAPPING = {
    # this should match .github/workflows/main.yml
    "AWS_ACCESS_KEY_ID": GITHUB_ENV_VAR_NAME_FOR_AWS_ACCESS_KEY_ID_FOR_GITHUB_CI,
    "AWS_SECRET_ACCESS_KEY": GITHUB_ENV_VAR_NAME_FOR_AWS_SECRET_ACCESS_KEY_FOR_GITHUB_CI,
}


def _read_env_file() -> dict[str, str]:
    """Parse a simple KEY=VALUE .env file."""
    if not ENV_FILE.exists():
        print(f"Error: {ENV_FILE} not found. Run create_access_key.py first.")
        sys.exit(1)
    result = {}
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, value = line.partition("=")
        result[key.strip()] = value.strip()
    return result


def main():
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        print("Error: GITHUB_TOKEN environment variable not set")
        sys.exit(1)

    env_vars = _read_env_file()

    owner, repo_name = get_github_repo_info()
    repo_fullname = f"{owner}/{repo_name}"
    print(f"Updating GitHub Actions secrets for: {repo_fullname}")

    gh = Github(auth=Auth.Token(github_token))
    try:
        repo = gh.get_repo(repo_fullname)
    except GithubException as e:
        print(f"Error: Could not access repository {repo_fullname}: {e}")
        sys.exit(1)

    for env_key, secret_name in SECRET_MAPPING.items():
        value = env_vars.get(env_key)
        if not value:
            print(f"Error: {env_key} not found in {ENV_FILE}")
            sys.exit(1)
        repo.create_secret(
            secret_name=secret_name,
            unencrypted_value=value,
            secret_type="actions",
        )
        print(f"  set {secret_name}")

    print("done")


if __name__ == "__main__":
    main()
