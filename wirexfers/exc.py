# -*- coding: utf-8 -*-
"""
wirexfers.exc
~~~~~~~~~~~~~

Exceptions used with WireXfers.

The base exception class is :class:`.WireXfersError`
"""

class WireXfersError(Exception):
    """Generic error class."""

class InvalidResponseError(WireXfersError):
    """
    Raised when an invalid payment response data is supplied to the response
    parser.
    """
