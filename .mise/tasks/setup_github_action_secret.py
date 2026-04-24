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

try:
    from github import Github, GithubException, Auth
except ImportError:
    print("Error: PyGithub not installed. Run: uv sync --extra mise")
    sys.exit(1)

from dotenv import load_dotenv
from boto_session_manager.tests.settings import GH_CI_AWS_ACCESS_KEY_ID_ENV_VAR
from boto_session_manager.tests.settings import GH_CI_AWS_SECRET_ACCESS_KEY_ENV_VAR

from utils import get_github_repo_info


def main():
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        print("Error: GITHUB_TOKEN environment variable not set")
        sys.exit(1)

    owner, repo_name = get_github_repo_info()
    repo_fullname = f"{owner}/{repo_name}"
    print(f"Updating GitHub Actions secrets for: {repo_fullname}")

    gh = Github(auth=Auth.Token(github_token))
    try:
        repo = gh.get_repo(repo_fullname)
    except GithubException as e:
        print(f"Error: Could not access repository {repo_fullname}: {e}")
        sys.exit(1)

    load_dotenv()

    repo.create_secret(
        secret_name=GH_CI_AWS_ACCESS_KEY_ID_ENV_VAR,
        unencrypted_value=os.environ[GH_CI_AWS_ACCESS_KEY_ID_ENV_VAR],
        secret_type="actions",
    )
    repo.create_secret(
        secret_name=GH_CI_AWS_SECRET_ACCESS_KEY_ENV_VAR,
        unencrypted_value=os.environ[GH_CI_AWS_SECRET_ACCESS_KEY_ENV_VAR],
        secret_type="actions",
    )

    print("done")


if __name__ == "__main__":
    main()
