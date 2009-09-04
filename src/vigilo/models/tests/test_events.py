# -*- coding: utf-8 -*-
"""Test suite for Event class"""
from vigilo.models import Events, Host, Service
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession
from nose.tools import assert_true
import re

class TestEvents(ModelTest):
    """Test de la table Events"""

    klass = Events
    attrs = {}

    def do_get_dependencies(self):
        """Generate some data for the test"""

        DBSession.add(Host(name = u"monhost"))
        DBSession.add(Service(name = u"monservice"))
        DBSession.flush()
        return dict(hostname = u"monhost", servicename = u"monservice")

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

    def __init__(self):
        ModelTest.__init__(self)

