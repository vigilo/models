# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for DowntimeStatus class"""
from datetime import datetime
from nose.tools import assert_equals

from vigilo.models.tables import Host, LowLevelService, User
from vigilo.models.tables import DowntimeStatus

from controller import ModelTest

class TestDowntimeStatus(ModelTest):
    """Unit test case for the ``DowntimeStatus`` model."""

    klass = DowntimeStatus

    attrs = dict(
        idstatus = 42,
        status = u"Foo",
    )

    def __init__(self):
        """Initialisation du test."""
        ModelTest.__init__(self)

    def test_statename_to_value(self):
        """Teste la récupération d'une valeur de statut par son nom."""
        status_id = self.obj.status_name_to_value(u'Foo')
        assert_equals(42, status_id)

    def test_value_to_statename(self):
        """Teste la récupération d'un nom de statut en connaissant son id."""
        status_name = self.obj.value_to_status_name(42)
        assert_equals(u'Foo', status_name)

