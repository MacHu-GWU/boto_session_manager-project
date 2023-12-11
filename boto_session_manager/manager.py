# -*- coding: utf-8 -*-

"""
Manage the underlying boto3 session and client.
"""

# standard library
import typing as T
import os
import uuid
import contextlib
from datetime import datetime, timezone, timedelta

# third party library
try:
    import boto3
    import boto3.session
    import botocore.session
except ImportError as e:  # pragma: no cover
    print("You probably need to install 'boto3' first.")

try:
    from botocore.credentials import (
        AssumeRoleCredentialFetcher,
        DeferredRefreshableCredentials,
    )
except ImportError as e:  # pragma: no cover
    print("The auto refreshable assume role session would not work.")

from .vendor.aws_sts import (
    mask_user_id,
    mask_aws_account_id,
    mask_iam_principal_arn,
    get_caller_identity,
    get_account_alias,
)

# modules from this project
from .services import AwsServiceEnum
from .clients import ClientMixin
from .sentinel import NOTHING, resolve_kwargs
from .exc import NoBotocoreCredentialError

if T.TYPE_CHECKING:  # pragma: no cover
    from botocore.client import BaseClient
    from boto3.resources.base import ServiceResource


class BotoSesManager(ClientMixin):
    """
    Boto3 session and client manager that use cache to create low level client.

    .. note::

        boto3.session.Session is a static object that won't talk to AWS endpoint.
        also session.client("s3") won't talk to AWS endpoint right away. The
        authentication only happen when a concrete API request called.

    .. versionadded:: 0.0.1

    .. versionchanged:: 0.0.4

        add ``default_client_kwargs`` arguments that set default keyword
        arguments for ``boto3.session.Session.client`` method.
    """

    def __init__(
        self,
        aws_access_key_id: T.Optional[str] = NOTHING,
        aws_secret_access_key: T.Optional[str] = NOTHING,
        aws_session_token: T.Optional[str] = NOTHING,
        region_name: T.Optional[str] = NOTHING,
        botocore_session: T.Optional["botocore.session.Session"] = NOTHING,
        profile_name: str = NOTHING,
        default_client_kwargs: dict = NOTHING,
        expiration_time: datetime = NOTHING,
    ):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_session_token = aws_session_token
        self.region_name = region_name
        if botocore_session is not NOTHING:  # pragma: no cover
            if not isinstance(botocore_session, botocore.session.Session):
                raise TypeError
        self.botocore_session: T.Optional["botocore.session.Session"] = botocore_session
        self.profile_name = profile_name
        self.expiration_time: datetime
        if expiration_time is NOTHING:
            self.expiration_time = datetime.utcnow().replace(
                tzinfo=timezone.utc
            ) + timedelta(days=365)
        else:
            self.expiration_time = expiration_time
        if default_client_kwargs is NOTHING:
            default_client_kwargs = dict()
        self.default_client_kwargs = default_client_kwargs

        self._boto_ses_cache: T.Optional["boto3.session.Session"] = NOTHING
        self._client_cache: T.Dict[str, "BaseClient"] = dict()
        self._resource_cache: T.Dict[str, "ServiceResource"] = dict()
        self._aws_user_id_cache: T.Optional[str] = NOTHING
        self._aws_account_id_cache: T.Optional[str] = NOTHING
        self._principal_arn_cache: T.Optional[str] = NOTHING
        self._aws_account_alias_cache: T.Optional[str] = NOTHING
        self._aws_region_cache: T.Optional[str] = NOTHING

    @property
    def boto_ses(self) -> "boto3.session.Session":
        """
        Get boto3 session from metadata.

        .. versionadded:: 1.0.2
        """
        if self._boto_ses_cache is NOTHING:
            self._boto_ses_cache = boto3.session.Session(
                **resolve_kwargs(
                    aws_access_key_id=self.aws_access_key_id,
                    aws_secret_access_key=self.aws_secret_access_key,
                    aws_session_token=self.aws_session_token,
                    region_name=self.region_name,
                    botocore_session=self.botocore_session,
                    profile_name=self.profile_name,
                )
            )
        return self._boto_ses_cache

    def _get_caller_identity(self):
        sts_client = self.get_client(AwsServiceEnum.STS)
        user_id, aws_account_id, arn = get_caller_identity(sts_client)
        self._aws_user_id_cache = user_id
        self._aws_account_id_cache = aws_account_id
        self._principal_arn_cache = arn

    @property
    def aws_account_user_id(self) -> str:
        """
        Get current aws account user id of the boto session.

        .. versionadded:: 1.6.1
        """
        if self._aws_user_id_cache is NOTHING:
            self._get_caller_identity()
        return self._aws_user_id_cache

    @property
    def masked_aws_account_user_id(self) -> str:
        """
        Get the masked current aws account user id of the boto session.

        .. versionadded:: 1.6.1
        """
        return mask_user_id(self.aws_account_user_id)

    @property
    def aws_account_id(self) -> str:
        """
        Get current aws account id of the boto session.

        .. versionadded:: 1.0.1
        """
        if self._aws_account_id_cache is NOTHING:
            self._get_caller_identity()
        return self._aws_account_id_cache

    @property
    def masked_aws_account_id(self) -> str:
        """
        Get the masked current aws account id of the boto session.

        .. versionadded:: 1.6.1
        """
        return mask_aws_account_id(self.aws_account_id)

    @property
    def principal_arn(self) -> str:
        """
        Get current principal arn of the boto session.

        .. versionadded:: 1.0.1
        """
        if self._principal_arn_cache is NOTHING:
            self._get_caller_identity()
        return self._principal_arn_cache

    @property
    def masked_principal_arn(self) -> str:
        """
        Get the masked principal arn of the boto session.

        .. versionadded:: 1.6.1
        """
        return mask_iam_principal_arn(self.principal_arn)

    @property
    def aws_region(self) -> str:
        """
        Get current aws region of the boto session.

        .. versionadded:: 0.0.1
        """
        if self._aws_region_cache is NOTHING:
            self._aws_region_cache = self.boto_ses.region_name
        return self._aws_region_cache

    @property
    def aws_account_alias(self) -> T.Optional[str]:
        """
        Get the first aws account alias of the boto session.

        .. versionadded:: 1.6.1
        """
        if self._aws_account_alias_cache is NOTHING:
            self._aws_account_alias_cache = get_account_alias(
                self.get_client(AwsServiceEnum.IAM)
            )
        return self._aws_account_alias_cache

    def print_who_am_i(self, masked: bool = True):  # pragma: no cover
        """
        Print the boto session AWS Account and IAM principal information.

        .. versionadded:: 1.6.1
        """
        if masked:
            print(f"User Id = {self.masked_aws_account_user_id}")
            print(f"AWS Account Id = {self.masked_aws_account_id}")
            print(f"Principal Arn = {self.masked_principal_arn}")
        else:
            print(f"User Id = {self.aws_account_user_id}")
            print(f"AWS Account Id = {self.aws_account_id}")
            print(f"Principal Arn = {self.principal_arn}")
        print(f"AWS Account Alias = {self.aws_account_alias}")
        print(f"AWS Region = {self.aws_region}")

    def get_client(
        self,
        service_name: str,
        region_name: str = NOTHING,
        api_version: str = NOTHING,
        use_ssl: bool = True,
        verify: T.Union[bool, str] = NOTHING,
        endpoint_url: str = NOTHING,
        aws_access_key_id: str = NOTHING,
        aws_secret_access_key: str = NOTHING,
        aws_session_token: str = NOTHING,
        config=None,
    ) -> "BaseClient":
        """
        Get aws boto client using cache.

        .. versionadded:: 0.0.1

        .. versionchanged:: 0.0.3

            add additional keyword arguments pass to
            ``boto3.session.Session.client()`` method.
        """
        try:
            return self._client_cache[service_name]
        except KeyError:
            client_kwargs = resolve_kwargs(
                region_name=region_name,
                api_version=api_version,
                use_ssl=use_ssl,
                verify=verify,
                endpoint_url=endpoint_url,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                aws_session_token=aws_session_token,
                config=config,
            )
            kwargs = dict(self.default_client_kwargs)
            if self.default_client_kwargs:  # pragma: no cover
                kwargs.update(client_kwargs)
            client = self.boto_ses.client(service_name, **kwargs)
            self._client_cache[service_name] = client
            return client

    def get_resource(
        self,
        service_name: str,
        region_name: str = NOTHING,
        api_version: str = NOTHING,
        use_ssl: bool = True,
        verify: T.Union[bool, str] = NOTHING,
        endpoint_url: str = NOTHING,
        aws_access_key_id: str = NOTHING,
        aws_secret_access_key: str = NOTHING,
        aws_session_token: str = NOTHING,
        config=NOTHING,
    ) -> "ServiceResource":
        """
        Get aws boto service resource using cache

        .. versionadded:: 0.0.2

        .. versionchanged:: 0.0.3

            add additional keyword arguments pass to
            ``boto3.session.Session.resource()`` method.
        """
        try:
            return self._resource_cache[service_name]
        except KeyError:
            resource_kwargs = resolve_kwargs(
                region_name=region_name,
                api_version=api_version,
                use_ssl=use_ssl,
                verify=verify,
                endpoint_url=endpoint_url,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                aws_session_token=aws_session_token,
                config=config,
            )
            kwargs = dict(self.default_client_kwargs)
            if self.default_client_kwargs:
                kwargs.update(resource_kwargs)
            resource = self.boto_ses.resource(service_name, **kwargs)
            self._resource_cache[service_name] = resource
            return resource

    def assume_role(
        self,
        role_arn: str,
        role_session_name: str = NOTHING,
        duration_seconds: int = 3600,
        tags: T.Optional[T.List[T.Dict[str, str]]] = NOTHING,
        transitive_tag_keys: T.Optional[T.List[str]] = NOTHING,
        external_id: str = NOTHING,
        mfa_serial_number: str = NOTHING,
        mfa_token: str = NOTHING,
        source_identity: str = NOTHING,
        region_name: str = NOTHING,
        auto_refresh: bool = False,
    ) -> "BotoSesManager":
        """
        Assume an IAM role, create another :class`BotoSessionManager` and return.

        :param auto_refresh: if True, the assumed role will be refreshed automatically.

        .. versionadded:: 0.0.1

        .. versionchanged:: 1.5.1

            add ``auto_refresh`` argument. note that it is using
            ``AssumeRoleCredentialFetcher`` and ``DeferredRefreshableCredentials``
            from botocore, which is not public API officially supported by botocore.
        """
        if role_session_name is NOTHING:
            role_session_name = uuid.uuid4().hex
        # if region_name is not specified, use the same region as the current session
        if region_name is NOTHING:
            region_name = self.aws_region
        # this branch cannot be tested regularly
        # it is tested in a separate integration test environment.
        if auto_refresh:  # pragma: no cover
            botocore_session = self.boto_ses._session
            credentials = botocore_session.get_credentials()
            # the get_credentials() method can return None
            # raise error explicitly
            if not credentials:
                raise NoBotocoreCredentialError

            credential_fetcher = AssumeRoleCredentialFetcher(
                client_creator=botocore_session.create_client,
                source_credentials=credentials,
                role_arn=role_arn,
                extra_args=resolve_kwargs(
                    RoleSessionName=role_session_name,
                    DurationSeconds=duration_seconds,
                    Tags=tags,
                    TransitiveTagKeys=transitive_tag_keys,
                    external_id=external_id,
                    SerialNumber=mfa_serial_number,
                    TokenCode=mfa_token,
                    SourceIdentity=source_identity,
                ),
            )

            assumed_role_credentials = DeferredRefreshableCredentials(
                refresh_using=credential_fetcher.fetch_credentials,
                method="assume-role",
            )
            assumed_role_botocore_session: "botocore.session.Session" = (
                botocore.session.get_session()
            )
            assumed_role_botocore_session._credentials = assumed_role_credentials
            return BotoSesManager(
                botocore_session=assumed_role_botocore_session,
                region_name=region_name,
                expiration_time=datetime(2099, 12, 31, 23, 59, 59, tzinfo=timezone.utc),
                default_client_kwargs=self.default_client_kwargs,
            )
        else:
            assume_role_kwargs = resolve_kwargs(
                RoleArn=role_arn,
                RoleSessionName=role_session_name,
                DurationSeconds=duration_seconds,
                Tags=tags,
                TransitiveTagKeys=transitive_tag_keys,
                external_id=external_id,
                SerialNumber=mfa_serial_number,
                TokenCode=mfa_token,
                SourceIdentity=source_identity,
            )
            sts_client = self.get_client(AwsServiceEnum.STS)
            res = sts_client.assume_role(**assume_role_kwargs)
            expiration_time = res["Credentials"]["Expiration"]
            bsm = self.__class__(
                aws_access_key_id=res["Credentials"]["AccessKeyId"],
                aws_secret_access_key=res["Credentials"]["SecretAccessKey"],
                aws_session_token=res["Credentials"]["SessionToken"],
                region_name=region_name,
                expiration_time=expiration_time,
                default_client_kwargs=self.default_client_kwargs,
            )
        return bsm

    def is_expired(self, delta: int = 0) -> bool:
        """
        Check if this boto session is expired.

        .. versionadded:: 0.0.1
        """
        return (
            datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(seconds=delta)
        ) >= self.expiration_time

    @contextlib.contextmanager
    def awscli(
        self,
        duration_seconds: int = 900,
        serial_number: T.Optional[str] = NOTHING,
        token_code: T.Optional[str] = NOTHING,
    ) -> "BotoSesManager":
        """
        Temporarily set up environment variable to pass the boto session
        credential to AWS CLI.

        Example::

            import subprocess

            bsm = BotoSesManager(...)

            with bsm.awscli():
                subprocess.run(["aws", "sts", "get-caller-identity"])

        Reference:

        - https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html

        .. versionadded:: 1.2.1
        """
        # save the existing env var state, and disable the existing env var
        env_names = [
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
            "AWS_SESSION_TOKEN",
            "AWS_REGION",
            "AWS_PROFILE",
        ]
        env_var = dict()
        for env_name in env_names:
            if env_name in os.environ:  # pragma: no cover
                env_var[env_name] = os.environ[env_name]
                os.environ.pop(env_name)
            else:
                env_var[env_name] = None

        # set environment variable for aws cli when you create this
        # boto session manager explicitly with ACCESS KEY and SECRET KEY
        if (
            (self.aws_access_key_id is not NOTHING)
            and (self.aws_secret_access_key is not NOTHING)
            and (self.aws_session_token is not NOTHING)
        ):
            os.environ["AWS_ACCESS_KEY_ID"] = self.aws_access_key_id
            os.environ["AWS_SECRET_ACCESS_KEY"] = self.aws_secret_access_key
            os.environ["AWS_SESSION_TOKEN"] = self.aws_session_token
            os.environ["AWS_REGION"] = self.aws_region
        elif (self.aws_access_key_id is not NOTHING) and (
            self.aws_secret_access_key is not NOTHING
        ):  # pragma: no cover
            os.environ["AWS_ACCESS_KEY_ID"] = self.aws_access_key_id
            os.environ["AWS_SECRET_ACCESS_KEY"] = self.aws_secret_access_key
            os.environ["AWS_REGION"] = self.aws_region
        elif self.profile_name is not NOTHING:
            os.environ["AWS_PROFILE"] = self.profile_name
            os.environ["AWS_REGION"] = self.aws_region
        else:
            kwargs = dict(
                DurationSeconds=duration_seconds,
            )
            if serial_number is not NOTHING:  # pragma: no cover
                kwargs["SerialNumber"] = serial_number
            if token_code is not NOTHING:  # pragma: no cover
                kwargs["TokenCode"] = token_code
            try:
                response = self.sts_client.get_session_token(**kwargs)
                aws_access_key_id = response["Credentials"]["AccessKeyId"]
                aws_secret_access_key = response["Credentials"]["SecretAccessKey"]
                aws_session_token = response["Credentials"]["SessionToken"]
                os.environ["AWS_ACCESS_KEY_ID"] = aws_access_key_id
                os.environ["AWS_SECRET_ACCESS_KEY"] = aws_secret_access_key
                os.environ["AWS_SESSION_TOKEN"] = aws_session_token
                os.environ["AWS_REGION"] = self.aws_region
            except Exception as e:  # pragma: no cover
                if "AccessDenied" in str(e):
                    # try to use the existing env var
                    # recover previous existing env var
                    for env_name, env_value in env_var.items():
                        if env_value is None:  # this env name is not exist before
                            if env_name in os.environ:
                                os.environ.pop(env_name)
                        else:
                            os.environ[env_name] = env_value
                else:  # pragma: no cover
                    raise e
        try:
            yield self
        finally:
            # recover previous existing env var
            for env_name, env_value in env_var.items():
                if env_value is None:  # this env name is not exist before
                    if env_name in os.environ:
                        os.environ.pop(env_name)
                else:
                    os.environ[env_name] = env_value

    def clear_cache(self):
        """
        Clear all the boto session and boto client cache.
        """
        self._boto_ses_cache = NOTHING
        self._client_cache.clear()
        self._resource_cache.clear()
        self._aws_account_id_cache = NOTHING
        self._aws_region_cache = NOTHING
