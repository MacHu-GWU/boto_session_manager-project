# -*- coding: utf-8 -*-

"""
Manage the underlying boto3 session and client.
"""

# standard library
import typing as T
import os
import json
import uuid
import warnings
import contextlib
from pathlib import Path
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

try:
    PATH_DEFAULT_SNAPSHOT = Path.home().joinpath(".bsm-snapshot.json")
except Exception as e:  # pragma: no cover
    PATH_DEFAULT_SNAPSHOT = None


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

    def create_boto_ses(self) -> "boto3.session.Session":
        """
        Create a new boto3 session object from the :class:`BotoSesManager`.

        .. versionadded:: 1.7.1
        """
        return boto3.session.Session(
            **resolve_kwargs(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                aws_session_token=self.aws_session_token,
                region_name=self.region_name,
                botocore_session=self.botocore_session,
                profile_name=self.profile_name,
            )
        )

    @property
    def boto_ses(self) -> "boto3.session.Session":
        """
        Get boto3 session from metadata. This is a cached property.

        .. versionadded:: 1.0.2
        """
        if self._boto_ses_cache is NOTHING:
            self._boto_ses_cache = self.create_boto_ses()
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
        Get current aws account user id of the boto session. This is a cached property.

        .. versionadded:: 1.6.1
        """
        if self._aws_user_id_cache is NOTHING:  # pragma: no cover
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
        Get current aws account id of the boto session. This is a cached property.

        .. versionadded:: 1.0.1
        """
        if self._aws_account_id_cache is NOTHING:  # pragma: no cover
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
        Get current principal arn of the boto session. This is a cached property.

        .. versionadded:: 1.0.1
        """
        if self._principal_arn_cache is NOTHING:  # pragma: no cover
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
        Get current aws region of the boto session. This is a cached property.

        .. versionadded:: 0.0.1
        """
        if self._aws_region_cache is NOTHING:
            self._aws_region_cache = self.boto_ses.region_name
        return self._aws_region_cache

    @property
    def aws_account_alias(self) -> T.Optional[str]:
        """
        Get the first aws account alias of the boto session. This is a cached property.

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

        .. versionchanged:: 1.7.1

            duration_seconds, serial_number and token_code arguments should not
            be used in this method, it should set the credential as it is,
            it should not create a new session, these arguments will be removed
            in 2024-03-31
        """
        if (
            serial_number is not NOTHING or token_code is not NOTHING
        ):  # pragma: no cover
            warnings.warn(
                "duration_seconds, serial_number and token_code arguments "
                "should not be used in this method, it should set the credential "
                "as it is, it should not create a new session, "
                "these arguments will be removed in 2024-03-31",
                DeprecationWarning,
            )

        # save the existing env var state, and disable the existing env var
        mapper = {
            "AWS_ACCESS_KEY_ID": None,
            "AWS_SECRET_ACCESS_KEY": None,
            "AWS_SESSION_TOKEN": None,
            "AWS_REGION": self.aws_region,
            "AWS_PROFILE": None,
        }
        cred = self.boto_ses.get_credentials()

        # set environment variable for aws cli when you create this
        # boto session manager explicitly with ACCESS KEY and SECRET KEY
        if self.profile_name is not NOTHING:
            mapper["AWS_PROFILE"] = self.profile_name
        elif cred.token is None:
            mapper["AWS_ACCESS_KEY_ID"] = cred.access_key
            mapper["AWS_SECRET_ACCESS_KEY"] = cred.secret_key
        else:
            mapper["AWS_ACCESS_KEY_ID"] = cred.access_key
            mapper["AWS_SECRET_ACCESS_KEY"] = cred.secret_key
            mapper["AWS_SESSION_TOKEN"] = cred.token

        # get existing env var
        existing = {}
        for k, v in mapper.items():
            existing[k] = os.environ.get(k)

        try:
            # set new env var
            for k, v in mapper.items():
                # v = None means delete this env var
                if v is None:
                    if k in os.environ:
                        os.environ.pop(k)
                else:
                    os.environ[k] = v
            yield self
        finally:
            # recover the original env var
            for k, v in existing.items():
                # v = None means this env var not exists at begin
                if v is None:
                    if k in os.environ:
                        os.environ.pop(k)
                else:
                    os.environ[k] = v

    def to_snapshot(self) -> dict:
        cred = self.boto_ses.get_credentials()
        snapshot = dict(
            region_name=self.aws_region,
            aws_access_key_id=cred.access_key,
            aws_secret_access_key=cred.secret_key,
        )
        if cred.token:
            snapshot["aws_session_token"] = cred.token
        return snapshot

    @classmethod
    def from_snapshot(cls, snapshot: dict):
        return cls(**snapshot)

    @classmethod
    def from_snapshot_file(
        cls,
        path: T.Union[str, Path] = PATH_DEFAULT_SNAPSHOT,
    ):
        if path is None:  # pragma: no cover
            raise EnvironmentError("your system may not support $HOME directory")
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Snapshot file not found: {path}")
        return cls.from_snapshot(json.loads(path.read_text()))

    @contextlib.contextmanager
    def temp_snapshot(
        self,
        path: T.Union[str, Path] = PATH_DEFAULT_SNAPSHOT,
    ) -> "BotoSesManager":
        """
        Temporarily back up the current boto session credentials to a file and
        automatically delete the backup file after the context manager exits.

        This is useful when you need to temporarily override environment variables
        for the default boto session but still want to access the original default
        boto session while those environment variables are missing.

        For example, if you use the :meth:`BotoSesManager.awscli` method to set
        the default boto session to an AWS account other than the default AWS CLI profile,
        and then you want to run some CLI commands. Now that the default boto session
        is set to the other AWS account, but you still want to access the original boto session,
        you can use this method to temporarily back up the original session and
        use the :meth:`BotoSesManager.from_snapshot_file` method to restore the original session.

        Example:

        .. code-block:: python

            # let's say the default profile is account A (acc_a)
            import subprocess

            bsm_default = BotoSesManager()
            bsm_acc_b = BotoSesManager(profile_name="acc_b")
            with bsm_default.temp_snapshot():
                with bsm_acc_b.awscli():
                    # now the default profile is account B (acc_b)
                    subprocess.run(["aws", "sts", "get-caller-identity"])
                    # you can use the ``from_snapshot_file`` method in ``my_script.py``
                    # to restore the default profile to account A (acc_a)
                    subprocess.run(["python", "my_script.py"])
        """
        if path is None:  # pragma: no cover
            raise EnvironmentError("your system may not support $HOME directory")
        path = Path(path)
        snapshot = self.to_snapshot()
        try:
            path.write_text(json.dumps(snapshot))
            yield self
        finally:
            if path.exists():
                path.unlink()

    def clear_cache(self):
        """
        Clear all the boto session and boto client cache.
        """
        self._boto_ses_cache = NOTHING
        self._client_cache.clear()
        self._resource_cache.clear()
        self._aws_user_id_cache = NOTHING
        self._aws_account_id_cache = NOTHING
        self._principal_arn_cache = NOTHING
        self._aws_account_alias_cache = NOTHING
        self._aws_region_cache = NOTHING