# -*- coding: utf-8 -*-

"""
Sentinel value for distinguishing "not provided" from ``None``.

In many boto3 APIs, ``None`` is a meaningful value (e.g. ``region_name=None``
means "let boto3 resolve the region from the environment"). A plain ``None``
default therefore cannot tell whether the caller explicitly passed ``None`` or
simply omitted the argument. The ``NOTHING`` sentinel fills that gap: any
parameter whose default is ``NOTHING`` is treated as *not provided* and will be
stripped out by :func:`resolve_kwargs` before forwarding to boto3.

``NOTHING`` is also used as the "uninitialised" marker for lazy-loaded cached
properties (e.g. ``_boto_ses_cache``, ``_aws_account_id_cache``), where the
cached value itself could legitimately be ``None``.

This module requires Python 3.10+. The previous implementation was borrowed from
the *boltons* library circa 2014 and carried legacy Python 2 compatibility code
(``__nonzero__``, ``sys._getframe`` for pickle support, dynamic inner classes).
None of that machinery is needed in modern Python, so it has been replaced with
the minimal implementation below.
"""

import typing as T


class _Nothing:
    """Sentinel singleton. Do **not** instantiate directly; use :data:`NOTHING`."""

    __slots__ = ()

    def __repr__(self) -> str:
        return "NOTHING"

    def __bool__(self) -> bool:
        return False


NOTHING = _Nothing()


def resolve_kwargs(
    _mapper: T.Optional[dict[str, str]] = None,
    **kwargs,
) -> dict[str, T.Any]:
    """Return a dict of *kwargs* with all ``NOTHING`` values removed.

    This lets callers write ``resolve_kwargs(region_name=self.region_name, ...)``
    and get back only the keys that were explicitly provided.

    :param _mapper: optional key-rename mapping, e.g.
        ``{"role_arn": "RoleArn"}`` translates the Python-style key to the
        AWS API name.
    """
    if _mapper is None:
        _mapper = dict()
    return {
        _mapper.get(key, key): value
        for key, value in kwargs.items()
        if value is not NOTHING
    }
