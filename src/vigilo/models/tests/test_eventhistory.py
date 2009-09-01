# -*- coding: utf-8 -*-
"""Test suite for EventHistory class"""
from vigilo.models import EventHistory, Host, Service, Events
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession

class TestEventHistory(ModelTest):
    """Test de la table EventHistory"""

    klass = EventHistory
    attrs = dict(type_action = u'Nagios update state', value = u'',
            text = u'', username = u'manager')

    def __init__(self):
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Generate some data for the test"""

        DBSession.add(Host(name = u"monhost"))
        DBSession.add(Service(name = u"monservice"))
        DBSession.flush()
        DBSession.add(Events(hostname = u"monhost", servicename = u"monservice"))
        DBSession.flush()
        return dict(idevent = DBSession.query(Events.idevent)[0].idevent)

