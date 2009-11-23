# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table ServiceGroup"""
from __future__ import absolute_import

from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Unicode, Integer
from sqlalchemy.orm import relation

from .vigilo_bdd_config import bdd_basename, DeclarativeBase

__all__ = ('ServiceGroup', )

class ServiceGroup(DeclarativeBase, object):

    __tablename__ = bdd_basename + 'servicegroup'

    servicename = Column(
        Integer,
        ForeignKey(bdd_basename + u'service.idservice'),
        primary_key=True, nullable=False, autoincrement=False,
    )

    idgroup = Column(
        Integer,
        ForeignKey(bdd_basename + u'group.idgroup'),
        primary_key=True, nullable=False, autoincrement=False,
    )

    services = relation('Service', back_populates='servicegroups', uselist=True,
        )

    groups = relation('Group', back_populates='servicegroups', uselist=True,
        )


    def __init__(self, **kwargs):
        """Initialise un groupe de services."""
        super(ServiceGroup, self).__init__(**kwargs)

    def __unicode__(self):
        return u'%s - %s' % (self.groupname, self.servicename)

