# -*- coding: utf-8 -*-

"""
Manage the underlying boto3 session and client.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

import boto3
from .services import AwsServiceEnum


class BotoSesManager:
    """
    Boto3 session and client manager that use cache to create low level client.

    .. note::

        boto3.session.Session is a static object that won't talk to AWS endpoint.
        also session.client("s3") won't talk to AWS endpoint right away. The
        authentication only happen when a concrete API request called.

    .. versionadded:: 1.0.1
    """

    def __init__(
        self,
        boto_ses: Optional['boto3.session.Session'] = None,
        expiration_time: datetime = datetime(2100, 1, 1, tzinfo=timezone.utc),
    ):
        if boto_ses is None:  # pragma: no cover
            boto_ses = boto3.session.Session()
        self.boto_ses = boto_ses
        self.expiration_time: datetime = expiration_time

        self._client_cache = dict()
        self._aws_account_id = None
        self._aws_region = None

    @property
    def aws_account_id(self) -> str:
        """
        Get current aws account id of the boto session

        .. versionadded:: 1.0.1
        """
        if self._aws_account_id is None:
            sts_client = self.get_client(AwsServiceEnum.STS)
            self._aws_account_id = sts_client.get_caller_identity()["Account"]
        return self._aws_account_id

    @property
    def aws_region(self) -> str:
        """
        Get current aws region of the boto session

        .. versionadded:: 0.0.1
        """
        if self._aws_region is None:
            self._aws_region = self.boto_ses.region_name
        return self._aws_region

    def get_client(self, service_name: str):
        """
        Get aws boto client using cache

        .. versionadded:: 0.0.1
        """
        try:
            return self._client_cache[service_name]
        except KeyError:
            client = self.boto_ses.client(service_name)
            self._client_cache[service_name] = client
            return client

    def assume_role(
        self,
        role_arn: str,
        role_session_name: str = None,
        duration_seconds: int = 3600,
        tags: list = None,
        transitive_tag_keys: list = None,
        external_id: str = None,
        mfa_serial_number: str = None,
        mfa_token: str = None,
        source_identity: str = None,
    ) -> 'BotoSesManager':
        """
        Assume an IAM role, create another :class`BotoSessionManager` and return.

        .. versionadded:: 0.0.1
        """
        if role_session_name is None:
            role_session_name = uuid.uuid4().hex
        kwargs = {
            k: v
            for k, v in dict(
                RoleArn=role_arn,
                RoleSessionName=role_session_name,
                DurationSeconds=duration_seconds,
                Tags=tags,
                TransitiveTagKeys=transitive_tag_keys,
                external_id=external_id,
                SerialNumber=mfa_serial_number,
                TokenCode=mfa_token,
                SourceIdentity=source_identity,
            ).items()
            if v is not None
        }
        sts_client = self.get_client(AwsServiceEnum.STS)
        res = sts_client.assume_role(**kwargs)
        boto_ses = boto3.session.Session(
            aws_access_key_id=res["Credentials"]["AccessKeyId"],
            aws_secret_access_key=res["Credentials"]["SecretAccessKey"],
            aws_session_token=res["Credentials"]["SessionToken"],
        )
        expiration_time = res["Credentials"]["Expiration"]
        bsm = self.__class__(
            boto_ses=boto_ses,
            expiration_time=expiration_time,
        )
        return bsm

    def is_expired(self) -> bool:
        """
        Check if this boto session is expired.

        .. versionadded:: 0.0.1
        """
        return datetime.utcnow().replace(tzinfo=timezone.utc) >= self.expiration_time
