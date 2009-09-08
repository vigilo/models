# -*- coding: utf-8 -*-
"""Test suite for Permission class"""
from vigilo.models import Permission
from vigilo.models.tests import ModelTest

class TestPermission(ModelTest):
    """Unit test case for the ``Permission`` model."""

    klass = Permission
    attrs = dict(
        permission_name = u"test_permission",
        )

    def __init__(self):
        ModelTest.__init__(self)
