# -*- coding: utf-8 -*-
"""Test suite for Event class"""
from vigilo.models import Event
from vigilo.models.tests import ModelTest

class TestEvent(ModelTest):
    """Test de la table Events"""

    klass = Events
    attrs = {}

    def do_get_dependencies(self):
        """Generate some data for the test"""

        DBSession.add(Host(name = "monhost"))
        DBSession.add(Service(name = "monservice"))
        DBSession.flush()
        return dict(hostname = "monhost", servicename = "monservice")

    def test_get_date(self):
        """La fonction GetDate doit renvoyer un objet formaté"""
        form1 = re.compile("^\w* \w* \d*:\d*:\d*$")
        form2 = re.compile("^\w* \d*:\d*:\d*$")
        assert_true(form1.match(self.obj.get_date("timestamp_active")) \
                or form2.match(self.obj.get_date("timestamp_active")))

    def test_get_since_date(self):
        """La fonction GetSinceDate doit renvoyer un objet formaté"""
        assert_true(re.compile("^\d*d \d*h \d'$").match(
            self.obj.get_since_date("timestamp_active")))

