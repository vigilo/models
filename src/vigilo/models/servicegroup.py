# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table ServiceGroup"""
from __future__ import absolute_import

from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Unicode
from sqlalchemy.orm import relation

from .vigilo_bdd_config import bdd_basename, DeclarativeBase

__all__ = ('ServiceGroup', )

class ServiceGroup(DeclarativeBase, object):

    __tablename__ = bdd_basename + 'servicegroup'

    servicename = Column(
        Unicode(255),
        ForeignKey(bdd_basename + u'service.name'),
        primary_key=True, nullable=False)

    groupname = Column(
        Unicode(255),
        ForeignKey(bdd_basename + u'group.name'),
        primary_key=True, nullable=False)

    services = relation('Service', backref='servicegroups', uselist=True,
        primaryjoin='ServiceGroup.servicename == Service.name')

    groups = relation('Group', backref='servicegroups', uselist=True,
        primaryjoin='ServiceGroup.groupname == Group.name')


    def __init__(self, **kwargs):
        """Initialise un groupe de services."""
        DeclarativeBase.__init__(self, **kwargs)

    def __unicode__(self):
        return u'%s - %s' % (self.groupname, self.servicename)

