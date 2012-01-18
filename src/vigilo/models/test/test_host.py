# -*- coding: utf-8 -*-
"""Test suite for Host class"""
from nose.tools import assert_equals

from vigilo.models.tables import Host, StateName
from vigilo.models.session import DBSession
from test_tag import TagTestMixin

from controller import ModelTest

class TestHost(ModelTest, TagTestMixin):
    """Test de la table host"""

    klass = Host
    attrs = {
        'name': u'myhost',
        'snmpcommunity': u'public',
        'description': u'My Host',
        'hosttpl': u'template',
        'address': u'127.0.0.1',
        'snmpport': 1234,
        'weight': 42,
    }

    def test_default_state(self):
        """L'état initial d'un hôte est 'OK'."""
        assert_equals(u'OK', StateName.value_to_statename(
            DBSession.query(self.klass).one().state.state))
