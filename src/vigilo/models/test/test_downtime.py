# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for Downtime class"""
from datetime import datetime

from vigilo.models.session import DBSession
from vigilo.models.demo import functions
from vigilo.models.tables import Host, LowLevelService, User
from vigilo.models.tables import Downtime, DowntimeStatus

from controller import ModelTest

class TestDowntime(ModelTest):
    """Unit test case for the ``Downtime`` model."""

    klass = Downtime

    attrs = dict(
        iddowntime = 42,
        entrytime = datetime.now(),
        comment = u"foo",
        start = datetime.now(),
        end = datetime.now()
    )

    def do_get_dependencies(self):
        """Insertion de données dans la base préalable aux tests."""
        ModelTest.do_get_dependencies(self)
        host = functions.add_host(u'myhost')
        service = functions.add_lowlevelservice(host, u'myservice')
        user = functions.add_user(
            u'foobar éçà',
            u'foobar@example.org',
            u'foo bar éçà',
            u'mdp éçà',
            None,
        )

        status = DowntimeStatus(
            status = u"Scheduled"
        )
        DBSession.add(status)
        DBSession.flush()

        return dict(supitem=service, user=user, status=status)
