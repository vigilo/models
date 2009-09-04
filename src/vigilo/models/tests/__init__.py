# -*- coding: utf-8 -*-
"""Unit test suite for the models of the application."""
from nose.tools import assert_equals
from vigilo.models.vigilo_bdd_config import metadata
from vigilo.models.session import DBSession

from os import path, environ
import sys
import nose

__all__ = ['ModelTest']

metadata.bind = DBSession.bind

#Create an empty database before we start our tests for this module
def setup():
    """Function called by nose on module load"""
    metadata.create_all()
    
#Teardown that database 
def teardown():
    """Function called by nose after all tests in this module ran"""
    metadata.drop_all()

class ModelTest(object):
    """Base unit test case for the models."""

    klass = None
    attrs = {}

    def __init__(self):
        object.__init__(self)

    def setup(self):
        """Set up the fixture used to test the model."""
        try:
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
        DBSession.rollback()
        del self.obj

    def do_get_dependencies(self):
        """
        Use this method to pull in other objects that need to be created
        for this object to be build properly
        """
        return {}

    def test_create_obj(self):
        pass

    def test_query_obj(self):
        obj = DBSession.query(self.klass).one()
        for key, value in self.attrs.iteritems():
            assert_equals(getattr(obj, key), value)

def runtests():
    """This is the method called when running unit tests."""
    # XXX hard-coded path.
    sys.argv[1:0] = ['--cover-inclusive',
                     '--cover-erase', '--cover-package', 'models',
                     'vigilo.models.tests']
    nose.main()
