#!/usr/bin/env python3

import aws_cdk as cdk
import aws_cdk.aws_iam as iam
from constructs import Construct

from boto_session_manager.tests.settings import TEST_IAM_USER_NAME
from boto_session_manager.tests.settings import TEST_IAM_ROLE_NAME


class Stack(cdk.Stack):
    def __init__(
        self,
        scope: Construct,
        prefix: str,
        **kwargs,
    ) -> None:
        self.prefix = prefix
        self.prefix_snake = prefix.replace("-", "_")
        self.prefix_slug = prefix.replace("_", "-")

        super().__init__(scope=scope, id=self.prefix_slug, **kwargs)

        # --- IAM User (for integration tests) ---
        self.iam_user = iam.User(
            scope=self,
            id="IamUser",
            user_name=TEST_IAM_USER_NAME,
        )

        # inline policy: allow sts/iam read + assume the test role
        self.iam_user.add_to_policy(
            iam.PolicyStatement(
                sid="AllowAssumeTestRole",
                actions=["sts:AssumeRole"],
                resources=[
                    f"arn:aws:iam::{cdk.Aws.ACCOUNT_ID}:role/{TEST_IAM_ROLE_NAME}"
                ],
            )
        )
        self.iam_user.add_to_policy(
            iam.PolicyStatement(
                sid="AllowStsAndIamRead",
                actions=[
                    "sts:GetAccessKeyInfo",
                    "sts:GetCallerIdentity",
                    "iam:ListAccountAliases",
                ],
                resources=["*"],
            )
        )

        # --- IAM Role (assumed by the user during tests) ---
        self.iam_role = iam.Role(
            scope=self,
            id="IamRole",
            role_name=TEST_IAM_ROLE_NAME,
            assumed_by=iam.AccountRootPrincipal(),
        )

        self.iam_role.add_to_policy(
            iam.PolicyStatement(
                sid="AllowStsAndIamRead",
                actions=[
                    "sts:GetAccessKeyInfo",
                    "sts:GetCallerIdentity",
                    "iam:ListAccountAliases",
                ],
                resources=["*"],
            )
        )


app = cdk.App()

Stack(
    scope=app,
    prefix="boto_session_manager-project",
)

app.synth()
