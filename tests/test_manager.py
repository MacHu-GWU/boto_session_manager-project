# -*- coding: utf-8 -*-

import pytest

import os
from boto_session_manager.manager import BotoSesManager, AwsServiceEnum

if "CI" in os.environ:  # pragma: no cover
    bsm = BotoSesManager(
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    )
else:  # pragma: no cover
    bsm = BotoSesManager(profile_name="aws_data_lab_open_source_boto_session_manager")


class TestBotoSesManager:
    def test_aws_account_id_and_region(self):
        _ = bsm.aws_account_id
        _ = bsm.aws_region

    def test_get_client(self):
        s3_client1 = bsm.get_client(AwsServiceEnum.S3)
        s3_client2 = bsm.get_client(AwsServiceEnum.S3)
        assert id(s3_client1) == id(s3_client2)

    def test_get_resource(self):
        s3_resource1 = bsm.get_resource(AwsServiceEnum.S3)
        s3_resource2 = bsm.get_resource(AwsServiceEnum.S3)
        assert id(s3_resource1) == id(s3_resource2)

    def test_is_expired(self):
        assert bsm.is_expired() is False

    def test_assume_role(self):
        # Test STS get caller identity
        sts_client = bsm.get_client(AwsServiceEnum.STS)

        aws_account_id = sts_client.get_caller_identity()["Account"]
        assert aws_account_id == bsm.aws_account_id

        # Test IAM role and Assumed IAM Role
        role_name = "project-boto_session_manager"
        bsm_assumed = bsm.assume_role(
            role_arn=f"arn:aws:iam::{aws_account_id}:role/{role_name}"
        )
        sts_client_assumed = bsm_assumed.get_client(AwsServiceEnum.STS)
        res = sts_client_assumed.get_caller_identity()
        assert res["Arn"].startswith(
            f"arn:aws:sts::{aws_account_id}:assumed-role/{role_name}"
        )
        assert bsm_assumed.expiration_time <= bsm.expiration_time


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
