# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table ServiceGroups"""
from __future__ import absolute_import

from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Unicode
from sqlalchemy.orm import relation

from .vigilo_bdd_config import bdd_basename, DeclarativeBase

class ServiceGroups(DeclarativeBase, object):

    __tablename__ = bdd_basename + 'servicegroups'

    servicename = Column(
        Unicode(255),
        ForeignKey(bdd_basename + u'service.name'),
        primary_key=True, nullable=False,
        info={'rum': {'field': 'Text'}})

    groupname = Column(
        Unicode(255),
        ForeignKey(bdd_basename + u'groups.name'),
        primary_key=True, nullable=False,
        info={'rum': {'field': 'Text'}})

#    service = relation('Service', backref='service_groups')
#    group = relation('Groups', backref='services')

    def __init__(self, **kwargs):
        """Initialise un groupe de services."""
        DeclarativeBase.__init__(self, **kwargs)


