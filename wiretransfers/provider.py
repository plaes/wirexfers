# -*- coding: utf-8 -*-
"""
wiretransfers.provider
~~~~~~~~~~~~~~~~~~~~~~

This module contains the payment provider implementations for Wiretransfers.
"""
class ProviderBase(object):
    """Base class that all provider implementations derive from."""

    def __init__(self, user, private_key, private_pass, public_key, endpoint, extra_info={}):

        #: User id for payment processor.
        self.user = user

        #: Endpoint address used to initiate payment requests.
        self.endpoint = endpoint

        #: Private key as an RSA key object (:py:class:`Crypto.PublicKey.RSA._RSAobj`)
        self.private_key = private_key

        #: Private key password
        self.private_pass = private_pass

        #: Public key as an RSA key object (:py:class:`Crypto.PublicKey.RSA._RSAobj`)
        self.pubkey = public_key

        #: Dictionary mapping containing extra user-supplied information.
        #: Can be used things like supplying provider url, etc.
        self.extra_info = extra_info

    def create_request(self, payment):
        pass

    def parse_response(self, args):
        pass

class LHV(ProviderBase):
    """
    LHV Bank payment protocol provider.

    Homepage: https://www.lhv.ee
    """
