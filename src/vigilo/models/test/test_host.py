# -*- coding: utf-8 -*-
# Copyright (C) 2011-2019 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for Host class"""

from nose.tools import assert_equals

from vigilo.models.tables import Host, StateName
from vigilo.models.session import DBSession

from vigilo.models.test.test_tag import TagTestMixin
from vigilo.models.test.controller import ModelTest

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
    }

    def test_default_state(self):
        """L'état initial d'un hôte est 'UP'."""
        assert_equals(u'UP', StateName.value_to_statename(
            DBSession.query(self.klass).one().state.state))
