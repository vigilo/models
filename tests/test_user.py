# -*- coding: utf-8 -*-
"""Test suite for User class"""
from nose.tools import eq_

from vigilo.models import User

from controller import ModelTest

class TestUser(ModelTest):
    """Unit test case for the ``User`` model."""

    klass = User
    attrs = dict(
        user_name = u"foobar",
        email = u"foobar@example.org",
        fullname = u'Foo bar',
    )

    def __init__(self):
        """Initialisation du test."""
        ModelTest.__init__(self)

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

