# -*- coding: utf-8 -*-
"""
wirexfers - an online payment library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

WireXfers is an online payments library, written in Python, providing
a simple common API for various online payment protocols (IPizza,
Solo/TUPAS).

:copyright: (c) 2012 Priit Laes
:license: ISC, see LICENSE for more details.
"""

__title__ = 'wirexfers'
__version__ = '0.0'
__author__ = 'Priit Laes'
__license__ = 'ISC'
__copyright__ = 'Copyright 2012 Priit Laes'

from .request import PaymentInfo, PaymentRequest
from .response import PaymentResponse
