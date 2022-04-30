# -*- coding: utf-8 -*-

import pytest
from boto_session_manager.manager import BotoSesManager, AwsServiceEnum

bsm = BotoSesManager()


class TestBotoSesManager:
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
        bsm1 = bsm.assume_role("arn:aws:iam::669508176277:role/sanhe-assume-role-for-iam-test")
        assert bsm1.expiration_time < bsm.expiration_time


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
