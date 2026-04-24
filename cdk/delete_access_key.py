# -*- coding: utf-8 -*-

"""
Delete all IAM access keys for the test user and remove .env.

Usage: python cdk/delete_access_key.py

Requires the ``AWS_PROFILE_FOR_CDK`` env var (set by mise.toml).
"""

from iam_access_key import delete_access_key_and_remove_env

delete_access_key_and_remove_env()
