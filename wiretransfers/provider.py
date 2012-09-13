# -*- coding: utf-8 -*-
"""
wiretransfers.provider
~~~~~~~~~~~~~~~~~~~~~~

This module contains the payment provider implementations for Wiretransfers.
"""

class ProviderBase(object):
    """Base class that all provider implementations derive from."""
    def __init__(self, user, endpoint, key, pubkey):
        pass

    def request(self, payment):
        pass

    def parse_response(self, args)
        pass
