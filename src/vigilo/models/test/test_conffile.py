# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for ConfItem class"""
from nose.tools import assert_equals, assert_not_equals

from vigilo.models.tables import ConfFile
from vigilo.models.test.controller import ModelTest

class TestConfFile(ModelTest):
    """Unit test case for the ``ConfFile`` model."""

    klass = ConfFile

    attrs = dict(
        name = u'dummy.xml',
    )

    def test_retrieval(self):
        """Récupération d'une instance de ConfFile par nom de fichier."""
        instance = self.klass.by_filename(self.attrs['name'])
        assert_equals(instance, self.obj)

    def test_on_the_fly_creation(self):
        """Création d'une instance de ConfFile à la volée."""
        # On ne doit pas créer de nouvelle instance s'il en existe déjà une.
        instance = self.klass.get_or_create(self.attrs['name'])
        assert_equals(instance, self.obj)
        # On doit par contre en créer une nouvelle sinon.
        instance2 = self.klass.get_or_create('copy-' + self.attrs['name'])
        assert_not_equals(instance, instance2)
        assert_equals(instance2.name, 'copy-' + self.attrs['name'])
