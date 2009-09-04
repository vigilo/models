# -*- coding: utf-8 -*-
"""Test suite for Host class"""
from vigilo.models import Host
from vigilo.models.tests import ModelTest

class TestHost(ModelTest):
    """Test de la table host"""

    klass = Host
    attrs = dict(name = u"monhost")

    def __init__(self):
        ModelTest.__init__(self)

