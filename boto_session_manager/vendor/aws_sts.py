# -*- coding: utf-8 -*-

import typing as T

if T.TYPE_CHECKING:
    import boto3
    from mypy_boto3_sts import STSClient
    from mypy_boto3_iam import IamClient

__version__ = "0.2.1"


def mask_user_id(user_id: str) -> str:
    """
    Example:

        >>> mask_user_id("A1B2C3D4GABCDEFGHIJKL")
        'A1B2***IJKL'
    """
    return user_id[:4] + "*" * 3 + user_id[-4:]


def mask_aws_account_id(aws_account_id: str) -> str:
    """
    Example:

        >>> mask_aws_account_id("123456789012")
        '12*********12'
    """
    return aws_account_id[:2] + "*" * 8 + aws_account_id[-2:]


def mask_iam_principal_arn(arn: str) -> str:
    """
    Mask an IAM principal ARN.

    Example:

        >>> mask_iam_principal_arn("arn:aws:iam::123456789012:role/role-name")
        'arn:aws:iam::12*********12:role/role-name'
    """
    parts = arn.split(":")
    parts[4] = mask_aws_account_id(parts[4])
    masked_arn = ":".join(parts)
    return masked_arn


def get_caller_identity(
    sts_client: "STSClient",
    masked: bool = False,
) -> T.Tuple[str, str, str]:
    res = sts_client.get_caller_identity()
    user_id = res["UserId"]
    account_id = res["Account"]
    arn = res["Arn"]
    if masked:
        user_id = mask_user_id(user_id)
        account_id = mask_aws_account_id(account_id)
        arn = mask_iam_principal_arn(arn)
    return user_id, account_id, arn


def get_account_alias(
    iam_client: "IamClient",
) -> T.Optional[str]:
    res = iam_client.list_account_aliases()
    return res.get("AccountAliases", [None])[0]
