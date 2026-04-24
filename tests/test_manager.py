# -*- coding: utf-8 -*-

from boto_session_manager.manager import BotoSesManager
from boto_session_manager.manager import AwsServiceEnum
from boto_session_manager.manager import PATH_DEFAULT_SNAPSHOT

import pytest

import os
import json
import subprocess

# fmt: off
from boto_session_manager.tests.settings import TEST_IAM_USER_NAME
from boto_session_manager.tests.settings import TEST_IAM_ROLE_NAME
from boto_session_manager.tests.settings import GH_CI_AWS_ACCESS_KEY_ID_ENV_VAR
from boto_session_manager.tests.settings import GH_CI_AWS_SECRET_ACCESS_KEY_ENV_VAR

if "CI" in os.environ:  # pragma: no cover
    IS_CI = True
# to test this on your local, make sure your DEFAULT AWS profile
# is NOT project_boto_session_manager
# and also the aws account is NOT the same as project_boto_session_manager
else:  # pragma: no cover
    IS_CI = False

    from dotenv import load_dotenv

    load_dotenv()

bsm_project = BotoSesManager(
    aws_access_key_id=os.environ[GH_CI_AWS_ACCESS_KEY_ID_ENV_VAR],
    aws_secret_access_key=os.environ[GH_CI_AWS_SECRET_ACCESS_KEY_ENV_VAR],
    region_name="us-east-1",
)

class TestBotoSesManager:
    def test_aws_account_id_and_region(self):
        _ = bsm_project.aws_account_user_id
        _ = bsm_project.masked_aws_account_user_id
        _ = bsm_project.aws_account_id
        _ = bsm_project.masked_aws_account_id
        _ = bsm_project.principal_arn
        _ = bsm_project.masked_principal_arn
        _ = bsm_project.aws_region
        _ = bsm_project.aws_account_alias

        bsm_assumed = bsm_project.assume_role(
            role_arn=f"arn:aws:iam::{bsm_project.aws_account_id}:role/{TEST_IAM_ROLE_NAME}"
        )
        _ = bsm_assumed.aws_account_user_id
        _ = bsm_assumed.masked_aws_account_user_id
        _ = bsm_assumed.aws_account_id
        _ = bsm_assumed.masked_aws_account_id
        _ = bsm_assumed.principal_arn
        _ = bsm_assumed.masked_principal_arn
        _ = bsm_assumed.aws_region
        _ = bsm_assumed.aws_account_alias

        # bsm.print_who_am_i()
        # bsm_assumed.print_who_am_i()

    def test_get_client(self):
        s3_client1 = bsm_project.get_client(AwsServiceEnum.S3)
        s3_client2 = bsm_project.get_client(AwsServiceEnum.S3)
        assert id(s3_client1) == id(s3_client2)

    def test_get_resource(self):
        s3_resource1 = bsm_project.get_resource(AwsServiceEnum.S3)
        s3_resource2 = bsm_project.get_resource(AwsServiceEnum.S3)
        assert id(s3_resource1) == id(s3_resource2)

    def test_clear_cache(self):
        _ = bsm_project.s3_client
        assert len(bsm_project._client_cache) >= 1

        bsm_project.clear_cache()
        assert len(bsm_project._client_cache) == 0

    def test_is_expired(self):
        assert bsm_project.is_expired() is False

    def test_assume_role(self):
        # Test STS get caller identity
        aws_account_id = bsm_project.sts_client.get_caller_identity()["Account"]
        assert aws_account_id == bsm_project.aws_account_id

        # Test IAM role and Assumed IAM Role
        bsm_assumed = bsm_project.assume_role(
            role_arn=f"arn:aws:iam::{aws_account_id}:role/{TEST_IAM_ROLE_NAME}"
        )
        sts_client_assumed = bsm_assumed.get_client(AwsServiceEnum.STS)
        res = sts_client_assumed.get_caller_identity()
        arn = f"arn:aws:sts::{aws_account_id}:assumed-role/{TEST_IAM_ROLE_NAME}"
        assert res["Arn"].startswith(arn)
        assert bsm_assumed.expiration_time <= bsm_project.expiration_time

    def _assert_aws_cli_env_var_exists(self):
        assert "AWS_ACCESS_KEY_ID" in os.environ
        assert "AWS_SECRET_ACCESS_KEY" in os.environ
        assert "AWS_SESSION_TOKEN" in os.environ
        assert "AWS_REGION" in os.environ

    def _assert_default_aws_cli_credential_is_different(self, bsm: BotoSesManager):
        args = ["aws", "sts", "get-caller-identity"]
        response = json.loads(
            subprocess.run(args, capture_output=True).stdout.decode("utf-8")
        )
        user_id, aws_account_id, arn = (
            response["UserId"],
            response["Account"],
            response["Arn"],
        )
        assert aws_account_id != bsm.aws_account_id
        assert not arn.endswith(TEST_IAM_USER_NAME)

        assert "AWS_ACCESS_KEY_ID" not in os.environ
        assert "AWS_SECRET_ACCESS_KEY" not in os.environ
        assert "AWS_SESSION_TOKEN" not in os.environ
        assert "AWS_REGION" not in os.environ

    def _ensure_default_aws_account_is_not_project_aws_account(self):
        bsm = BotoSesManager()
        if bsm_project == bsm.aws_account_id:
            raise EnvironmentError(
                "For this test, the default AWS account cannot be the same as "
                "the project AWS account"
            )

    @pytest.mark.skipif(
        IS_CI,
        reason="we don't want to expose real AWS credentials in CI",
    )
    def test_cli_context_manager_with_arguments(self):
        self._ensure_default_aws_account_is_not_project_aws_account()

        # the bsm object is using the profile "project_boto_session_manager"
        # which is an IAM user.
        # however, the aws cli uses different AWS profile
        self._assert_default_aws_cli_credential_is_different(bsm_project)

        def get_caller_identity() -> tuple[str, str, str]:
            args = ["aws", "sts", "get-caller-identity"]
            response = json.loads(
                subprocess.run(args, capture_output=True).stdout.decode("utf-8")
            )
            user_id, aws_account_id, arn = (
                response["UserId"],
                response["Account"],
                response["Arn"],
            )
            return user_id, aws_account_id, arn

        # iam user
        # the aws cli uses the same AWS profile as the bsm object
        with bsm_project.awscli():
            user_id, aws_account_id, arn = get_caller_identity()
            assert aws_account_id == bsm_project.aws_account_id
            assert arn.endswith(f"user/{TEST_IAM_USER_NAME}")
            assert "AWS_ACCESS_KEY_ID" in os.environ
            assert "AWS_SECRET_ACCESS_KEY" in os.environ
            assert "AWS_SESSION_TOKEN" not in os.environ
            assert "AWS_PROFILE" not in os.environ

        self._assert_default_aws_cli_credential_is_different(bsm_project)

        # assume role
        bsm_assumed = bsm_project.assume_role(
            role_arn=f"arn:aws:iam::{aws_account_id}:role/{TEST_IAM_ROLE_NAME}"
        )
        # the aws cli uses the sts session token as the same as the assumed role
        with bsm_assumed.awscli():
            user_id, aws_account_id, arn = get_caller_identity()
            assert aws_account_id == bsm_assumed.aws_account_id
            assert f"assumed-role/{TEST_IAM_ROLE_NAME}" in arn
            assert "AWS_ACCESS_KEY_ID" in os.environ
            assert "AWS_SECRET_ACCESS_KEY" in os.environ
            assert "AWS_SESSION_TOKEN" in os.environ
            assert "AWS_PROFILE" not in os.environ

        self._assert_default_aws_cli_credential_is_different(bsm_project)

        bsm_default = BotoSesManager()

        with bsm_default.awscli():
            user_id, aws_account_id, arn = get_caller_identity()
            assert bsm_default.aws_account_id == aws_account_id
            assert "AWS_ACCESS_KEY_ID" in os.environ
            assert "AWS_SECRET_ACCESS_KEY" in os.environ
            if bsm_default.boto_ses.get_credentials().token:
                assert "AWS_SESSION_TOKEN" in os.environ
            else:
                assert "AWS_SESSION_TOKEN" not in os.environ
            assert "AWS_PROFILE" not in os.environ

    @pytest.mark.skipif(
        IS_CI,
        reason="we don't want to expose real AWS credentials in CI",
    )
    def test_temp_snapshot(self):
        self._ensure_default_aws_account_is_not_project_aws_account()

        bsm_default = BotoSesManager()
        assert bsm_default.aws_account_id != bsm_project.aws_account_id

        with bsm_default.temp_snapshot():
            with bsm_project.awscli():
                bsm_new = BotoSesManager()
                assert bsm_new.aws_account_id == bsm_project.aws_account_id
                bsm_origin = BotoSesManager.from_snapshot_file()
                assert bsm_origin.aws_account_id == bsm_default.aws_account_id

        assert PATH_DEFAULT_SNAPSHOT.exists() is False


if __name__ == "__main__":
    from boto_session_manager.tests import run_cov_test

    run_cov_test(
        __file__,
        "boto_session_manager.manager",
        preview=False,
    )
