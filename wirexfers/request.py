# -*- coding: utf-8 -*-
"""
wirexfers.request
~~~~~~~~~~~~~~~~~

This module implements a PaymentRequest class which provides us the
payment request forms.
"""
class PaymentInfo(object):
    """Payment information required for :class:`~.PaymentRequest`."""
    def __init__(self, amount, message, refnum):
        #: Payment amount as string, uses ``.`` as decimal point separator.
        self.amount = amount
        #: Message used for payment description.
        self.message = message
        #: Reference number.
        self.refnum = refnum

class PaymentRequest(object):
    """PaymentRequest class.

    :param provider: Payment provider
    :type provider: :class:`~wirexfers.providers.ProviderBase`.
    :param info: Payment information
    :type info: :class:`~wirexfers.PaymentInfo`.
    :param return_urls: Dictionary of return URLs. Depends on the specific
                        provider, but generally ``{'return': ... }`` is
                        required.
    :type return_urls: :class:`Dict`

    Raises :exc:`ValueError` when invalid configuration is detected.
    """
    # TODO: language, payment receiver's account info
    def __init__(self, provider, info, return_urls):
        #: :class:`~.providers.ProviderBase` that handles the payment request.
        self.provider = provider

        #: :class:`~.PaymentInfo` containing various payment information (sum, etc..)
        self.info = info

        if 'return' not in return_urls:
            raise ValueError

        # Make preloaded keys possible
        from Crypto import Random
        Random.atfork()

        #: List containing ``(name, value)`` tuples for HTML-form setup.
        self.form = provider._sign_request(info, return_urls)
