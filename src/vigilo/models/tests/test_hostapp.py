# -*- coding: utf-8 -*-
"""Test suite for HostApplication & HostBusApplication classes"""
from vigilo.models import HostApplication, HostBusApplication, \
                            Application, Host
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession

class TestHostApplication(ModelTest):
    """Unit test case for the ``HostApplication`` model."""

    klass = HostApplication
    attrs = {}

    def __init__(self):
        """Initialisation du test."""
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Generate some data for the test"""
        host = Host(
            name=u'myhost',
            checkhostcmd=u'halt -f',
            snmpcommunity=u'public',
            description=u'My Host',
            hosttpl=u'template',
            mainip=u'127.0.0.1',
            snmpport=u'1234',
            weight=42,
        )
        DBSession.add(host)
        DBSession.flush()

        app = Application(
            name=u'Nagios',
        )
        DBSession.add(app)
        DBSession.flush()

        return dict(host=host, application=app, appserver=host)

class TestHostBusApplication(ModelTest):
    """Unit test case for the ``HostBusApplication`` model."""

    klass = HostBusApplication
    attrs = {
        'jid': u'foo@bar',
    }

    def __init__(self):
        """Initialisation du test."""
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Generate some data for the test"""
        host = Host(
            name=u'myhost',
            checkhostcmd=u'halt -f',
            snmpcommunity=u'public',
            description=u'My Host',
            hosttpl=u'template',
            mainip=u'127.0.0.1',
            snmpport=u'1234',
            weight=42,
        )
        DBSession.add(host)
        DBSession.flush()

        app = Application(
            name=u'Nagios',
        )
        DBSession.add(app)
        DBSession.flush()

        return dict(host=host, application=app, appserver=host)

