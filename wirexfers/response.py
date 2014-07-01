# -*- coding: utf-8 -*-
"""
    wirexfers.response
    ~~~~~~~~~~~~~~~~~~

    This module implements a PaymentResponse class used for payment validation.

    :copyright: (c) 2012-2014 Priit Laes
    :license: ISC, see LICENSE for more details.
"""

class PaymentResponse(object):
    """PaymentResponse class."""

    def __init__(self, provider, data, successful=False):
        #: :class:`~wirexfers.providers.ProviderBase` that handles the payment request.
        self.provider = provider
        #: Whether payment response is successful (some providers don't provide this status,
        #: therefore allow setting it from the view)
        self.successful = successful
        #: Dictionary containing payment-related data, specific to provider
        self.data = data
