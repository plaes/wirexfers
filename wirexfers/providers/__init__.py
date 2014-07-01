# -*- coding: utf-8 -*-
"""
wirexfers.provider
~~~~~~~~~~~~~~~~~~

Base classes for implementing payment providers.
"""
from wirexfers import PaymentRequest

class KeyChainBase(object):
    """Base class for protocol-specific key handling."""
    def __init__(self):
        raise NotImplementedError('Provider should implement its own keychain.')

class ProviderBase(object):
    """Base class for all payment providers."""

    def __init__(self, user, keychain, endpoint, extra_info={}):

        #: User id for payment processor.
        self.user = user

        #: Endpoint address used to initiate payment requests.
        self.endpoint = endpoint

        #: Protocol-specific keychain implementation -
        #: :class:`wirexfers.providers.KeyChainBase`
        self.keychain = keychain

        #: Dictionary containing extra user-supplied information.
        #: Can be used for supplying provider url, etc.
        self.extra_info = extra_info

    def __call__(self, payment, return_urls):
        """
        Create and return a payment request.

        :param payment: payment information
        :type payment: :class:`~wirexfers.PaymentInfo`
        :rtype: :class:`~wirexfers.PaymentRequest`
        """
        return PaymentRequest(self, payment, return_urls)

    def parse_response(self, data):
        """Parse the payment request.

        :param form: Raw payment response data.
        """
        raise NotImplementedError('Provider should implement its own response handler')

    def _sign_request(self, info, return_urls):
        """Sign the payment request."""
        raise NotImplementedError('Provider should implement its own signing')
