# -*- coding: utf-8 -*-
"""
    wirexfers.exc
    ~~~~~~~~~~~~~

    Exceptions used with WireXfers.

    The base exception class is :class:`.WireXfersError`

    :copyright: (c) 2012-2014 Priit Laes
    :license: ISC, see LICENSE for more details.
"""

class WireXfersError(Exception):
    """Generic error class."""

class InvalidResponseError(WireXfersError):
    """
    Raised when an invalid payment response data is supplied to the response
    parser.
    """
