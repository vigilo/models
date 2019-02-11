# -*- coding: utf-8 -*-
# Copyright (C) 2011-2019 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for Permission class"""
from vigilo.models.tables import Permission

from vigilo.models.test.controller import ModelTest

class TestPermission(ModelTest):
    """Unit test case for the ``Permission`` model."""

    klass = Permission
    attrs = dict(
        permission_name = u"test_permission",
        )

    def __init__(self):
        ModelTest.__init__(self)

