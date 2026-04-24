# -*- coding: utf-8 -*-

"""
Manage IAM access keys for the integration-test user.

The ``AWS_PROFILE_FOR_CDK`` env var (set by mise.toml) controls which AWS
profile is used for all IAM operations.
"""

import os
from pathlib import Path

import boto3

from settings import IAM_USER_NAME

ENV_FILE = Path(__file__).parent.parent / ".env"  # MAKE SURE THIS IS RIGHT


def _get_iam_client():
    profile = os.environ.get("AWS_PROFILE_FOR_CDK")  # THIS IS FROM mise.toml
    session = boto3.Session(profile_name=profile)
    return session.client("iam")


def create_access_key_and_write_env() -> None:
    """Delete any existing access keys, create a fresh one, write to ``.env``."""
    iam = _get_iam_client()

    # delete existing keys to avoid the 2-key-per-user limit
    existing = iam.list_access_keys(UserName=IAM_USER_NAME)
    for meta in existing["AccessKeyMetadata"]:
        iam.delete_access_key(
            UserName=IAM_USER_NAME,
            AccessKeyId=meta["AccessKeyId"],
        )
        print(f"deleted access key {meta['AccessKeyId']}")

    # create a fresh key — secret key only appears in this response
    resp = iam.create_access_key(UserName=IAM_USER_NAME)
    ak = resp["AccessKey"]

    ENV_FILE.write_text(
        f"AWS_ACCESS_KEY_ID={ak['AccessKeyId']}\n"
        f"AWS_SECRET_ACCESS_KEY={ak['SecretAccessKey']}\n"
    )
    print(f"wrote credentials to {ENV_FILE}")


def delete_access_key_and_remove_env() -> None:
    """Delete all access keys for the user and remove ``.env``."""
    iam = _get_iam_client()

    existing = iam.list_access_keys(UserName=IAM_USER_NAME)
    for meta in existing["AccessKeyMetadata"]:
        iam.delete_access_key(
            UserName=IAM_USER_NAME,
            AccessKeyId=meta["AccessKeyId"],
        )
        print(f"deleted access key {meta['AccessKeyId']}")

    if ENV_FILE.exists():
        ENV_FILE.unlink()
        print(f"removed {ENV_FILE}")
