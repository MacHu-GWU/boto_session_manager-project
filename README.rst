..
    .. image:: https://readthedocs.org/projects/boto_session_manager/badge/?version=latest
        :target: https://boto_session_manager.readthedocs.io/index.html
        :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/boto_session_manager-project/workflows/CI/badge.svg
    :target: https://github.com/MacHu-GWU/boto_session_manager-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/boto_session_manager-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/boto_session_manager-project

.. image:: https://img.shields.io/pypi/v/boto_session_manager.svg
    :target: https://pypi.python.org/pypi/boto_session_manager

.. image:: https://img.shields.io/pypi/l/boto_session_manager.svg
    :target: https://pypi.python.org/pypi/boto_session_manager

.. image:: https://img.shields.io/pypi/pyversions/boto_session_manager.svg
    :target: https://pypi.python.org/pypi/boto_session_manager

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/boto_session_manager-project

------

..
    .. image:: https://img.shields.io/badge/Link-Document-blue.svg
        :target: https://boto_session_manager.readthedocs.io/index.html

    .. image:: https://img.shields.io/badge/Link-API-blue.svg
        :target: https://boto_session_manager.readthedocs.io/py-modindex.html

    .. image:: https://img.shields.io/badge/Link-Source_Code-blue.svg
        :target: https://boto_session_manager.readthedocs.io/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/boto_session_manager-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/boto_session_manager-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/boto_session_manager-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/boto_session_manager#files


Welcome to ``boto_session_manager`` Documentation
==============================================================================


Feature
------------------------------------------------------------------------------
**Boto Client Enum**

Provide an Enum class to access the aws service name to create boto client.

.. code-block:: python

    from boto_session_manager import BotoSesManager, AwsServiceEnum

    bsm = BotoSesManager()
    s3_client = bsm.s3_client

.. image:: https://user-images.githubusercontent.com/6800411/215315251-162886ee-067e-4441-882e-f2641b0997ca.gif

One click to jump to the documentation:

.. image:: https://user-images.githubusercontent.com/6800411/215315252-52d89d6a-d234-4635-b412-044894a46442.gif


**Cached Client**

Once an boto session is defined, each AWS Service client should be created only once in most of the case. ``boto_session_manager.BotoSesManager.get_client(service_name)`` allow you to fetch the client object from cache if possible.

.. code-block:: python

    from boto_session_manager import BotoSesManager, AwsServiceEnum

    bsm = BotoSesManager()
    s3_client1 = bsm.get_client(AwsServiceEnum.S3)
    s3_client2 = bsm.get_client(AwsServiceEnum.S3)
    assert id(s3_client1) = id(s3_client2)
    
Or you can just do:

.. code-block:: python

    bsm.s3_client.list_buckets() # it cache the client when needed


**Assume Role**

Create another boto session manager based on an assumed IAM role. Allow you to check if it is expired and maybe renew later.

.. code-block:: python

    bsm_assumed = bsm.assume_role("arn:aws:iam::669508176277:role/sanhe-assume-role-for-iam-test")
    sts_client = bsm_assumed.get_client(AwsServiceEnum.sts)
    print(sts_client.get_caller_identity())

    print(bsm_assumed.is_expired())

**AWS CLI context manager**

Suppose you have a boto session manager defined in python, sometime you want to run aws cli from Python using `subprocess <https://docs.python.org/3/library/subprocess.html>`_ library. You can use ``boto_session_manager.BotoSesManager.awscli()`` context manager to setup temp credential for AWS CLI.

.. code-block:: python

    import subprocess

    bsm = BotoSesManager(...)

    with bsm.awscli():
        subprocess.run(["aws", "sts", "get-caller-identity"])


.. _install:

Install
------------------------------------------------------------------------------

``boto_session_manager`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install boto_session_manager

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade boto_session_manager
