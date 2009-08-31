# -*- coding: utf-8 -*-
"""Test suite for UserGroup class"""
from vigilo.models import UserGroup
from vigilo.models.tests import ModelTest

class TestUserGroup(ModelTest):
    """Unit test case for the ``Group`` model."""
    klass = UserGroup
    attrs = dict(
        group_name = u"test_group",
        )

    def __init__(self):
        ModelTest.__init__(self)

