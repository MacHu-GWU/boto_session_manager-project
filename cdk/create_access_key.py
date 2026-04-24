# -*- coding: utf-8 -*-

"""
Create a fresh IAM access key and write credentials to .env.

Usage: python cdk/create_access_key.py

Requires the ``AWS_PROFILE_FOR_CDK`` env var (set by mise.toml).
"""

from iam_access_key import create_access_key_and_write_env

create_access_key_and_write_env()
