# -*- coding: utf-8 -*-
# Copyright (C) 2006-2012 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for ConfItem class"""
from nose.tools import assert_equals

from vigilo.models.demo import functions
from vigilo.models.tables import ConfItem
from vigilo.models.test.controller import ModelTest

class TestServiceConfItem(ModelTest):
    """Unit test case for the ``ConfItem`` model."""

    klass = ConfItem

    attrs = dict(
        name = u'retry_interval',
        value = u"4"
    )

    def do_get_dependencies(self):
        """Insertion de données dans la base préalable aux tests."""
        ModelTest.do_get_dependencies(self)
        host = functions.add_host(u'myhost')
        service = functions.add_lowlevelservice(host, u'myservice')
        return dict(supitem=service)

    def test_get_by_host_service_confitem_name(self):
        ob = ConfItem.by_host_service_confitem_name(
            u'myhost', u'myservice', self.attrs['name'])
        assert_equals('4', ob.value)



class TestHostConfItem(ModelTest):
    """Unit test case for the ``ConfItem`` model."""

    klass = ConfItem

    attrs = dict(
        name = u"check_interval",
        value = u"5"
    )

    def do_get_dependencies(self):
        """Insertion de données dans la base préalable aux tests."""
        ModelTest.do_get_dependencies(self)
        host = functions.add_host(u'myhost')
        return dict(supitem=host)

    def test_get_by_host_confitem_name(self):
        ob = ConfItem.by_host_confitem_name(u'myhost', self.attrs['name'])
        assert_equals('5', ob.value)
