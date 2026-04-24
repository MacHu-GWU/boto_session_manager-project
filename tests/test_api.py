# -*- coding: utf-8 -*-

from boto_session_manager import api


def test():
    _ = api

    _ = api.BotoSesManager
    _ = api.PATH_DEFAULT_SNAPSHOT
    _ = api.AwsServiceEnum


if __name__ == "__main__":
    from boto_session_manager.tests import run_cov_test

    run_cov_test(
        __file__,
        "boto_session_manager.api",
        preview=False,
    )
