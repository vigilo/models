# -*- coding: utf-8 -*-
# Copyright (C) 2011-2018 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for Tag class"""

from nose.tools import assert_equals

from vigilo.models.tables import Tag
from vigilo.models.session import DBSession

class TagTestMixin(object):
    def test_delete_tag(self):
        """Suppression d'un tag."""
        self.obj.tags['foo'] = 'bar'
        DBSession.flush()
        assert_equals(1, len(self.obj.tags))

        del self.obj.tags['foo']
        DBSession.flush()
        assert_equals(0, len(self.obj.tags))

    def test_null_tags(self):
        """Affectation de la valeur None à un Tag."""
        self.obj.tags['foo'] = None
        DBSession.flush()

    def test_by_supitem_and_tag_name(self):
        """Récupération d'un tag par supitem et nom."""
        self.obj.tags['foo'] = 'bar'
        DBSession.flush()
        tag = Tag.by_supitem_and_tag_name(self.obj, 'foo')
        assert_equals(tag.value, self.obj.tags['foo'])
