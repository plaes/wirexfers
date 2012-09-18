# -*- coding: utf-8 -*-
"""
wirexfers.response
~~~~~~~~~~~~~~~~~~

This module implements a PaymentResponse class used for payment validation.
"""

class PaymentResponse(object):
    """PaymentResponse class."""

    def __init__(self, provider, is_valid, data):
        #: :class:`~wirexfers.providers.ProviderBase` that handles the payment request.
        self.provider = provider
        #: Whether payment response is valid
        self.is_valid = is_valid
        #: Dictionary containing payment-related data, specific to provider
        self.data = data
