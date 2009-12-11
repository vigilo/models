# -*- coding: utf-8 -*-
"""Test suite for Host class"""
from vigilo.models import Host
from vigilo.models.tests import ModelTest

class TestHost(ModelTest):
    """Test de la table host"""

    klass = Host
    attrs = {
        'name': u'myhost',
        'checkhostcmd': u'halt -f',
        'snmpcommunity': u'public',
        'description': u'My Host',
        'hosttpl': u'template',
        'mainip': u'127.0.0.1',
        'snmpport': 1234,
        'weight': 42,
    }

    def __init__(self):
        ModelTest.__init__(self)

