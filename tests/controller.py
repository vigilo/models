# -*- coding: utf-8 -*-
"""Unit test suite for the models of the application."""
from nose.tools import assert_equals
from vigilo.models.statename import StateName
from vigilo.models.configure import DBSession, metadata, configure_db

from os import path, environ
import sys
import nose

__all__ = ['ModelTest', 'setup_db', 'teardown_db']

#Create an empty database before we start our tests for this module
def setup_db():
    """Crée toutes les tables du modèle dans la BDD."""
    from ConfigParser import SafeConfigParser
    parser = SafeConfigParser()
    parser.read('test.ini')

    settings = dict(parser.items('vigilo.models'))

    configure_db(settings, 'sqlalchemy.')
#    db_basename = settings['db_basename']
    metadata.create_all()
    
#Teardown that database 
def teardown_db():
    """Supprime toutes les tables du modèle de la BDD."""
    metadata.drop_all()

class ModelTest(object):
    """Base unit test case for the models."""

    klass = None
    attrs = {}

    def __init__(self):
        """Initialise une suite de tests sur un object du modèle."""
        object.__init__(self)
        self.obj = None

    def setup(self):
        """Set up the fixture used to test the model."""
        try:
            print "Class being tested:", self.klass
            new_attrs = {}
            new_attrs.update(self.attrs)
            new_attrs.update(self.do_get_dependencies())
            self.obj = self.klass(**new_attrs)
            DBSession.add(self.obj)
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

    def do_get_dependencies(self):
        """
        Use this method to pull in other objects that need to be created
        for this object to be build properly
        """
        DBSession.add(StateName(statename=u'OK', order=0))
        DBSession.add(StateName(statename=u'UNKNOWN', order=1))
        DBSession.add(StateName(statename=u'WARNING', order=2))
        DBSession.add(StateName(statename=u'CRITICAL', order=3))
        DBSession.flush()
        return {}

    def test_create_obj(self):
        """Teste la création de l'objet."""
        pass

    def test_query_obj(self):
        """Vérifie les données insérées."""
        obj = DBSession.query(self.klass).one()
        for key, value in self.attrs.iteritems():
            assert_equals(getattr(obj, key), value)

