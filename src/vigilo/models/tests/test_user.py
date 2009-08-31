# -*- coding: utf-8 -*-
"""Test suite for User class"""
from nose.tools import eq_

from vigilo.models import User
from vigilo.models.tests import ModelTest
from vigilo.common.conf import settings

class TestUser(ModelTest):
    """Unit test case for the ``User`` model."""

    klass = User
    attrs = dict(
        user_name = u"foobar",
        email = u"foobar@example.org"
        )

    def __init__(self):
        ModelTest.__init__(self)

    def test_obj_creation_username(self):
        """The obj constructor must set the user name right"""
        eq_(self.obj.user_name, u"foobar")

    def test_obj_creation_email(self):
        """The obj constructor must set the email right"""
        eq_(self.obj.email, u"foobar@example.org")

    def test_no_permissions_by_default(self):
        """User objects should have no permission by default."""
        eq_(len(self.obj.permissions), 0)

    def test_getting_by_email(self):
        """Users should be fetcheable by their email"""
        him = User.by_email_address(u"foobar@example.org")
        eq_(him, self.obj)

    def test_getting_by_user_name(self):
        """Users should be fetcheable by their username"""
        him = User.by_user_name(u"foobar")
        eq_(him, self.obj)

    def test_default_language(self):
        """Users' default language should be the configuration-defined one"""
        default_language = settings['VIGILO_ALL_DEFAULT_LANGUAGE']
        eq_(self.obj.language, default_language)

