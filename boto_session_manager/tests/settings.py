# -*- coding: utf-8 -*-

# fmt: off
ENV_VAR_NAME_FOR_AWS_PROFILE_FOR_CDK = "AWS_PROFILE_FOR_CDK"
TEST_IAM_USER_NAME = "project-boto_session_manager"
TEST_IAM_ROLE_NAME = "project-boto_session_manager"
GH_CI_AWS_ACCESS_KEY_ID_ENV_VAR = "AWS_ACCESS_KEY_ID_FOR_GITHUB_CI"
GH_CI_AWS_SECRET_ACCESS_KEY_ENV_VAR = "AWS_SECRET_ACCESS_KEY_FOR_GITHUB_CI"
# fmt: on


def load_bsm_project():
    import os
    from dotenv import load_dotenv

    from ..manager import BotoSesManager

    load_dotenv()

    bsm_project = BotoSesManager(
        aws_access_key_id=os.environ[GH_CI_AWS_ACCESS_KEY_ID_ENV_VAR],
        aws_secret_access_key=os.environ[GH_CI_AWS_SECRET_ACCESS_KEY_ENV_VAR],
        region_name="us-east-1",
    )
    return bsm_project
