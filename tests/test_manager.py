# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx
from boto_session_manager.manager import BotoSesManager

bsm = BotoSesManager()


class TestBotoSesManager:
    def test_is_expired(self):
        assert bsm.is_expired() is False

    def test_assume_role(self):
        bsm1 = bsm.assume_role("arn:aws:iam::669508176277:role/sanhe-assume-role-for-iam-test")
        assert bsm1.expiration_time < bsm.expiration_time


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
