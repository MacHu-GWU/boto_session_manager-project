.. _release_history:

Release and Version History
==============================================================================


1.1.2 (Planned)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add refreshable session support

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


1.1.1 (2022-11-20)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- the first API stable version

**Minor Improvements**

- add ``delta`` arguments for :meth:`~boto_session_manager.manager.BotoSesManager.is_expired` method. allow to check if the session will expire in X seconds.


0.0.4 (2022-05-20)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``default_client_kwargs`` argument for :class:`boto_session_manager.manager.BotoSesManager`.

**Miscellaneous**

- use `localstack <https://localstack.cloud/>`_ for unit test.


0.0.3 (2022-05-16)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add additional keyword arguments for :meth:`boto_session_manager.manager.BotoSesManager.get_client` method

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.0.2 (2022-04-30)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- now :class:`boto_session_manager.manager.BotoSesManager`
- add :meth:`boto_session_manager.manager.BotoSesManager.get_resource` method


0.0.1 (2022-04-26)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- First release
- Add :class:`boto_session_manager.manager.BotoSessionManager` class
- Add :class:`boto_session_manager.services.BotoSessionManager` class
