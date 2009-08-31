# -*- coding: utf-8 -*-
"""Test suite for EventHistory class"""
from vigilo.models import EventHistory
from vigilo.models.tests import ModelTest

class TestEventHistory(ModelTest):
    """Test de la table EventHistory"""

    klass = EventHistory
    attrs = dict(type_action = 'Nagios update state', value = '',
            text = '', username = 'manager')

    def __init__(self):
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Generate some data for the test"""

        DBSession.add(Host(name = "monhost"))
        DBSession.add(Service(name = "monservice"))
        DBSession.flush()
        DBSession.add(Events(hostname = "monhost", servicename = "monservice"))
        DBSession.flush()
        return dict(idevent = DBSession.query(Events.idevent)[0].idevent)

