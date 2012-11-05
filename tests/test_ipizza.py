#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Path hack :)
import os, sys
sys.path.insert(0, os.path.abspath('..'))

import unittest

import wirexfers
from wirexfers.providers.ipizza import EELHVProvider, EESwedBankProvider

class IPizzaTestCase(unittest.TestCase):
    """Test cases for IPizza protocol providers."""
    # We can currently only test mac generation (no signing/verifying) due
    # to private/public key traits
    def testEELHVrequest(self):
        # pangalink.net
        data = [('VK_SERVICE', u'1002'), ('VK_VERSION', u'008'), \
                ('VK_SND_ID', 'uid217929'), ('VK_STAMP', '1348812094'), \
                ('VK_AMOUNT', '1.01'), ('VK_CURR', u'EUR'), \
                ('VK_REF', '1232'), ('VK_MSG', u'\u65e5\u672c\u8a9e'), \
                ('VK_CHARSET', 'UTF-8')]
        fields = ('SERVICE', 'VERSION', 'SND_ID', \
                  'STAMP', 'AMOUNT', 'CURR', 'REF', 'MSG')
        _mac = u'0041002003008009uid21792901013488120940041.01003EUR0041232009日本語'.encode('utf-8')
        assert EELHVProvider._build_mac(fields, dict(data)) == _mac

    def testEELHVResponse(self):
        # pangalink.net
        data = dict([('VK_MAC', u'...'), ('VK_AMOUNT', u'1.01'), \
                     ('VK_CHARSET', u'UTF-8'), ('VK_AUTO', u'N'), \
                     ('VK_SERVICE', u'1101'), ('VK_STAMP', u'1348813282'), \
                     ('nupp', u'Tagasi kaupmehe juurde'), \
                     ('VK_VERSION', u'008'), ('VK_REF', u'1232'), \
                     ('VK_SND_ID', u'LHV'), ('VK_REC_ID', u'uid217929'), \
                     ('VK_SND_NAME', u'T\xf5\xf5ger Le\xf5p\xe4\xf6ld'), \
                     ('VK_SND_ACC', u'771234567897'), ('VK_T_NO', u'16022'), \
                     ('VK_REC_NAME', u'wirefoo'), \
                     ('VK_MSG', u'\u65e5\u672c\u8a9e'), \
                     ('VK_REC_ACC', u''), ('VK_T_DATE', u'28.09.2012'), \
                     ('VK_CURR', u'EUR')])
        fields = ('SERVICE', 'VERSION', 'SND_ID', 'REC_ID', 'STAMP', \
                  'T_NO', 'AMOUNT', 'CURR', 'REC_ACC', 'REC_NAME', 'SND_ACC', \
                  'SND_NAME', 'REF', 'MSG', 'T_DATE')

        _hash = u'0041101003008003LHV009uid2179290101348813282005160220041.01003EUR000007wirefoo012771234567897020Tõõger Leõpäöld0041232009日本語01028.09.2012'.encode('utf-8')
        assert EELHVProvider._build_mac(fields, data) == _hash
