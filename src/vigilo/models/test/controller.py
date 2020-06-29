# -*- coding: utf-8 -*-
# Copyright (C) 2006-2020 CS GROUP – France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Unit test suite for the models of the application."""
from __future__ import print_function
from nose.tools import assert_equals
from vigilo.models.session import DBSession, metadata
from vigilo.models.tables import StateName

__all__ = ['ModelTest', 'setup_db', 'teardown_db', 'Options']

class Options(object):
    """
    Simule les options telles qu'elles pourraient être
    créées par C{OptionParser}.
    """

    def __init__(self, options=None, **kwargs):
        if options is None:
            options = {}
        self.__dict__.update(options, **kwargs)

def populate_statename():
    DBSession.add(StateName(statename=u'OK', order=1))
    DBSession.add(StateName(statename=u'UNKNOWN', order=2))
    DBSession.add(StateName(statename=u'WARNING', order=3))
    DBSession.add(StateName(statename=u'CRITICAL', order=4))
    DBSession.add(StateName(statename=u'UP', order=1))
    DBSession.add(StateName(statename=u'UNREACHABLE', order=2))
    DBSession.add(StateName(statename=u'DOWN', order=4))
    DBSession.flush()

#Create an empty database before we start our tests for this module
def setup_db():
    """Crée toutes les tables du modèle dans la BDD."""
    # On crée les tables, puis les vues.
    mapped_tables = metadata.tables.copy()
    views = {}
    for tablename in mapped_tables:
        info = mapped_tables[tablename].info or {}
        if info.get('vigilo_view'):
            views[tablename] = mapped_tables[tablename]
    for view in views:
        del mapped_tables[view]

    metadata.create_all(tables=mapped_tables.itervalues())
    metadata.create_all(tables=views.values())
    populate_statename()

#Teardown that database
def teardown_db():
    """Supprime toutes les tables du modèle de la BDD."""
    metadata.drop_all()

class ModelTest(object):
    """Base unit test case for the models."""

    klass = object
    attrs = {}

    def __init__(self):
        """Initialise une suite de tests sur un object du modèle."""
        object.__init__(self)
        self.obj = None

    def setup(self):
        """Set up the fixture used to test the model."""
        setup_db()
        try:
            print("Class being tested:", self.klass)
            new_attrs = {}
            new_attrs.update(self.attrs)
            new_attrs.update(self.do_get_dependencies())
            self.obj = self.klass(**new_attrs)
            self.obj = DBSession.merge(self.obj)
            DBSession.flush()
            return self.obj
        except:
            DBSession.rollback()
            raise

    def tearDown(self):
        """Tear down the fixture used to test the model."""
        del self.obj
        DBSession.rollback()
        DBSession.expunge_all()
        teardown_db()

    def do_get_dependencies(self):
        """
        Use this method to pull in other objects that need to be created
        for this object to be built properly.
        """
        return {}

    def test_create_obj(self):
        """Teste la création de l'objet."""
        pass

    def test_query_obj(self):
        """Vérifie les données insérées."""
        obj = DBSession.query(self.klass).one()
        for key, value in self.attrs.iteritems():
            assert_equals(getattr(obj, key), value)
