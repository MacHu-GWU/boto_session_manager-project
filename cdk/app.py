#!/usr/bin/env python3

import aws_cdk as cdk
import aws_cdk.aws_iam as iam
from constructs import Construct

from settings import IAM_USER_NAME


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

        self.iam_user = iam.User(
            scope=self,
            id="IamUser",
            user_name=IAM_USER_NAME,
        )


app = cdk.App()

Stack(
    scope=app,
    prefix="boto_session_manager-project",
)

app.synth()
