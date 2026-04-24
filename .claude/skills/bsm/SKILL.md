---
name: bsm
description: >
  How to use the boto_session_manager library. Use when writing Python code that interacts with AWS via boto3,
  creating boto sessions, assuming IAM roles, managing AWS credentials, or using typed AWS service clients.
  Trigger when: code imports boto_session_manager, user mentions BotoSesManager, or user asks how to use bsm.
---

# boto_session_manager Usage Guide

`boto_session_manager` is a high-level wrapper around `boto3` that manages AWS sessions, clients, and resources
with caching, type hints, assume-role support, and credential management utilities.

**Import namespace:**

```python
from boto_session_manager.api import BotoSesManager
from boto_session_manager.api import AwsServiceEnum  # optional, for get_client()/get_resource()
```

If you need more detail about the source code, index files under `boto_session_manager/` in this project.

---

## 1. Creating a BotoSesManager

`BotoSesManager` wraps a `boto3.Session` and is the single entry point for all features.

```python
from boto_session_manager.api import BotoSesManager

# Default credential chain (env vars, ~/.aws/credentials, instance profile, etc.)
bsm = BotoSesManager()

# Named AWS profile
bsm = BotoSesManager(profile_name="my_aws_profile")

# Explicit credentials
bsm = BotoSesManager(
    aws_access_key_id="AKIA...",
    aws_secret_access_key="SECRET...",
    aws_session_token="TOKEN...",  # optional, for temporary credentials
    region_name="us-east-1",
)

# Default kwargs passed to every boto3 client (e.g. LocalStack endpoint)
bsm = BotoSesManager(
    default_client_kwargs={"endpoint_url": "http://localhost:4566"},
)
```

## 2. Typed Client Properties (400+ services)

Every AWS service has a typed lazy property on `BotoSesManager`. The client is created on first access and cached.

```python
bsm = BotoSesManager()

bsm.s3_client            # S3Client (fully typed)
bsm.ec2_client           # EC2Client
bsm.lambda_client        # LambdaClient
bsm.dynamodb_client      # DynamoDBClient
bsm.sqs_client           # SQSClient
bsm.iam_client           # IAMClient
bsm.sts_client           # STSClient
# ... 400+ more

# Methods are auto-completed with correct argument types
bsm.s3_client.list_buckets()
bsm.s3_client.put_object(Bucket="my-bucket", Key="key", Body=b"data")
```

> **Tip:** Install `pip install "boto3-stubs[all]"` for full IDE auto-complete and type checking.

## 3. Cached Client and Resource

Clients and resources are created once and reused from cache.

```python
from boto_session_manager.api import BotoSesManager, AwsServiceEnum

bsm = BotoSesManager()

# get_client() with AwsServiceEnum
s3_client_1 = bsm.get_client(AwsServiceEnum.S3)
s3_client_2 = bsm.get_client(AwsServiceEnum.S3)
assert id(s3_client_1) == id(s3_client_2)  # same object from cache

# get_resource() for boto3 resource interface
s3_resource = bsm.get_resource(AwsServiceEnum.S3)

# The typed property shortcut uses the same cache:
assert id(bsm.s3_client) == id(s3_client_1)
```

## 4. AWS Identity Inspection

Cached properties to query current AWS identity. Each calls STS/IAM once on first access.

```python
bsm = BotoSesManager()

# Identity info (cached)
bsm.aws_account_id          # "123456789012"
bsm.aws_account_user_id     # "AIDA..."
bsm.principal_arn            # "arn:aws:iam::123456789012:user/my-user"
bsm.aws_region               # "us-east-1"
bsm.aws_account_alias        # "my-account-alias" or None

# Masked versions for safe logging
bsm.masked_aws_account_id          # "12**********12"
bsm.masked_aws_account_user_id     # "AI**...DA"
bsm.masked_principal_arn            # "arn:aws:iam::12**********12:user/my-user"

# Print a human-friendly summary
bsm.print_who_am_i()          # masked by default
bsm.print_who_am_i(masked=False)  # show real values
```

## 5. Assume IAM Role

Returns a new independent `BotoSesManager` operating under the assumed role.

```python
bsm = BotoSesManager()

bsm_assumed = bsm.assume_role(
    role_arn="arn:aws:iam::111122223333:role/my-role",
    duration_seconds=3600,  # default 1 hour
)

# Full BotoSesManager — all features work
bsm_assumed.sts_client.get_caller_identity()

# Optional parameters
bsm_assumed = bsm.assume_role(
    role_arn="arn:aws:iam::111122223333:role/my-role",
    role_session_name="my-session",
    tags=[{"Key": "Project", "Value": "demo"}],
    external_id="my-external-id",
    region_name="eu-west-1",  # switch region at the same time
)
```

### Auto-refreshable assumed role

For long-running processes, credentials refresh transparently before expiry.

```python
bsm_assumed = bsm.assume_role(
    role_arn="arn:aws:iam::111122223333:role/my-role",
    duration_seconds=900,   # 15-minute tokens
    auto_refresh=True,      # botocore refreshes them automatically
)
# Session keeps working indefinitely as long as source credentials are valid
```

> **Note:** `auto_refresh` uses botocore's internal `DeferredRefreshableCredentials` — not a public API.

## 6. Check Session Expiration

```python
bsm_assumed = bsm.assume_role(
    role_arn="arn:aws:iam::111122223333:role/my-role",
    duration_seconds=3600,
)

bsm_assumed.is_expired()          # False (just created)
bsm_assumed.is_expired(delta=300) # True if < 5 min remaining
```

## 7. AWS CLI Context Manager

Temporarily injects credentials into `os.environ` for AWS CLI subprocesses. Restores original env on exit.

```python
import subprocess
from boto_session_manager.api import BotoSesManager

bsm = BotoSesManager(profile_name="my_aws_profile")

with bsm.awscli():
    # os.environ now has AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
    subprocess.run(["aws", "sts", "get-caller-identity"])

# env vars are restored to their original state here

# Also works with assumed-role sessions (AWS_SESSION_TOKEN is set automatically)
bsm_assumed = bsm.assume_role(role_arn="arn:aws:iam::111122223333:role/my-role")
with bsm_assumed.awscli():
    subprocess.run(["aws", "s3", "ls"])
```

## 8. Credential Snapshot

Serialize credentials to a dict or JSON file, and restore them in another process.

```python
from boto_session_manager.api import BotoSesManager

bsm = BotoSesManager()

# Serialize to dict
snapshot = bsm.to_snapshot()
# {"region_name": "us-east-1", "aws_access_key_id": "AKIA...", ...}

# Restore from dict
bsm_restored = BotoSesManager.from_snapshot(snapshot)

# temp_snapshot() — writes to ~/.bsm-snapshot.json, deletes on exit
bsm_default = BotoSesManager()
bsm_other = BotoSesManager(profile_name="other_account")

with bsm_default.temp_snapshot():
    with bsm_other.awscli():
        # env points to other_account, but child processes can recover original:
        #   bsm_origin = BotoSesManager.from_snapshot_file()
        subprocess.run(["python", "my_child_script.py"])
# ~/.bsm-snapshot.json is automatically deleted

# Restore from file (in child process)
bsm_origin = BotoSesManager.from_snapshot_file()  # default: ~/.bsm-snapshot.json
bsm_origin = BotoSesManager.from_snapshot_file("/path/to/snapshot.json")
```

## 9. Clear Cache

Resets all internal caches (session, clients, resources, identity). Use when credentials change.

```python
bsm = BotoSesManager()
bsm.s3_client.list_buckets()  # client created and cached
bsm.clear_cache()             # all caches cleared
bsm.s3_client.list_buckets()  # fresh client created
```

---

## Quick Reference

| What you want | Code |
|---|---|
| Default session | `BotoSesManager()` |
| Named profile | `BotoSesManager(profile_name="...")` |
| Explicit creds | `BotoSesManager(aws_access_key_id="...", aws_secret_access_key="...", region_name="...")` |
| S3 client | `bsm.s3_client` |
| Any client | `bsm.get_client(AwsServiceEnum.SERVICE_NAME)` |
| Any resource | `bsm.get_resource(AwsServiceEnum.SERVICE_NAME)` |
| Account ID | `bsm.aws_account_id` |
| Masked account ID | `bsm.masked_aws_account_id` |
| Current region | `bsm.aws_region` |
| Account alias | `bsm.aws_account_alias` |
| Who am I | `bsm.print_who_am_i()` |
| Assume role | `bsm.assume_role(role_arn="...")` |
| Auto-refresh role | `bsm.assume_role(role_arn="...", auto_refresh=True)` |
| Check expiration | `bsm_assumed.is_expired(delta=300)` |
| CLI env injection | `with bsm.awscli(): ...` |
| Save snapshot | `bsm.to_snapshot()` / `bsm.temp_snapshot()` |
| Load snapshot | `BotoSesManager.from_snapshot(d)` / `BotoSesManager.from_snapshot_file()` |
| Clear caches | `bsm.clear_cache()` |