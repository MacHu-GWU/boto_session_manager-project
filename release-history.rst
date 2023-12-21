.. _release_history:

Release and Version History
==============================================================================


Backlog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


1.7.1 (2023-12-20)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add :meth:`~boto_session_manager.manager.BotoSesManager.create_boto_ses` method.
- add :meth:`~boto_session_manager.manager.BotoSesManager.to_snapshot` method.
- add :meth:`~boto_session_manager.manager.BotoSesManager.from_snapshot` method.
- add :meth:`~boto_session_manager.manager.BotoSesManager.from_snapshot_file` method.
- add :meth:`~boto_session_manager.manager.BotoSesManager.temp_snapshot` method.
- add ``PATH_DEFAULT_SNAPSHOT`` constant to public API.
- add support and test for 3.11, 3.12.
- drop support for 3.6. test only covers 3.7+, older versions may still work.

**Minor Improvements**

- add support for some edge case for the :meth:`~boto_session_manager.manager.BotoSesManager.awscli` method. Also identified that ``duration_seconds``, ``serial_number`` and ``token_code`` arguments should not be used in this method. It should set the credential as it is, it should not create a new session, these arguments will be removed in 2024-03-31

**Miscellaneous**

- Improve doc string.


1.6.1 (2023-12-10)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add :meth:`~boto_session_manager.manager.BotoSesManager.aws_account_user_id` property method.
- add :meth:`~boto_session_manager.manager.BotoSesManager.masked_aws_account_user_id` property method.
- add :meth:`~boto_session_manager.manager.BotoSesManager.masked_aws_account_id` property method.
- add :meth:`~boto_session_manager.manager.BotoSesManager.principal_arn` property method.
- add :meth:`~boto_session_manager.manager.BotoSesManager.masked_principal_arn` property method.
- add :meth:`~boto_session_manager.manager.BotoSesManager.aws_account_alias` property method.
- add :meth:`~boto_session_manager.manager.BotoSesManager.print_who_am_i` method.


1.5.4 (2023-07-14)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Miscellaneous**

- AWS occasionally updates the boto3 client name on their website, making some of the old ``bsm.${service_name}_client`` unavailable. We add alias for those old service name to maintain backward compatibility.
- Add ``sagemaker_a2i_runtime_client`` alias.


1.5.3 (2023-05-25)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Bugfixes**

- fix bug that the :meth:`~boto_session_manager.manager.BotoSesManager.awscli` method doesn't work properly when using profile name, or using IAM role on EC2, lambda, etc...


1.5.2 (2023-05-11)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Minor Improvements**

- add ``region_name`` argument for :meth:`~boto_session_manager.manager.BotoSesManager.assume_role` method. If it is not given, then reuse the AWS region of the base session.


1.5.1 (2023-04-14)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add auto refreshable session support (beta). Note that it is using ``AssumeRoleCredentialFetcher`` and ``DeferredRefreshableCredentials`` from botocore, which is not public API officially supported by botocore.

**Minor Improvements**

- Use Sentinel ``NOTHING`` instead of ``None`` to remove the ambiguity of ``None`` value.


1.4.3 (2023-04-14)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Miscellaneous**

- Add ``boto3`` as explicit dependency.
- Change license from MIT to Apache 2.0


1.4.2 (2023-03-24)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Bugfixes**

- Fix a bug that the client object cannot locate the right boto3 stubs.


1.4.1 (2023-03-24)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Now all the client and it's methods support auto complete and type hint. You have to do ``pip install "boto3-stubs[all]"`` to enable "Client method auto complete" and "Arguments type hint" features.

**Bugfixes**

- Fix a bug that :meth:`~boto_session_manager.manager.BotoSesManager.awscli()`` context manager doesn't work properly.


1.3.2 (2023-01-31)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add boto3 documentation link in doc string


1.3.1 (2022-12-10)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Allow to call :meth:`~boto_session_manager.manager.BotoSesManager.clear_cache()` to clear all cached boto session and client.
- Add ton's of property method to access the cached boto client.
- Update the list of AWS service to the latest (as of 2022-12-10), which are 333 services.


1.2.2 (2022-12-10)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Miscellaneous**

- Now ``boto_session_manager`` doesn't force to install ``boto3`` when installing itself. You have to manage your ``boto3`` installation separately.


1.2.1 (2022-11-20)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add :meth:`~boto_session_manager.manager.BotoSesManager.awscli` context manager to pass boto session credential to AWS CLI.


1.1.1 (2022-11-20)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- The first API stable version

**Minor Improvements**

- Add ``delta`` arguments for :meth:`~boto_session_manager.manager.BotoSesManager.is_expired` method. allow to check if the session will expire in X seconds.


0.0.4 (2022-05-20)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add ``default_client_kwargs`` argument for :class:`boto_session_manager.manager.BotoSesManager`.

**Miscellaneous**

- Use `localstack <https://localstack.cloud/>`_ for unit test.


0.0.3 (2022-05-16)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add additional keyword arguments for :meth:`boto_session_manager.manager.BotoSesManager.get_client` method


0.0.2 (2022-04-30)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Now the public API becomes :class:`boto_session_manager.manager.BotoSesManager`
- Add :meth:`boto_session_manager.manager.BotoSesManager.get_resource` method


0.0.1 (2022-04-26)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- First release
- Add :class:`boto_session_manager.manager.BotoSessionManager` class
- Add :class:`boto_session_manager.services.BotoSessionManager` class
