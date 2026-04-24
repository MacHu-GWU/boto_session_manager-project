#!/usr/bin/env python3

import aws_cdk as cdk
from constructs import Construct


prefix = ""


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


app = cdk.App()

Stack(
    scope=app,
    prefix="boto_session_manager-project",
)

app.synth()
