# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table HostGroup"""
from __future__ import absolute_import

from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Unicode, Integer
from sqlalchemy.orm import relation

from .vigilo_bdd_config import bdd_basename, DeclarativeBase

__all__ = ('HostGroup', )

class HostGroup(DeclarativeBase, object):

    __tablename__ = bdd_basename + 'hostgroup'

    hostname = Column(
        Unicode(255),
        ForeignKey(bdd_basename + u'host.name'),
        primary_key=True, nullable=False)

    idgroup = Column(
        Integer,
        ForeignKey(bdd_basename + u'group.idgroup'),
        primary_key=True, nullable=False, autoincrement=False)

    hosts = relation('Host', back_populates='hostgroups', uselist=True,
        )

    groups = relation('Group', back_populates='hostgroups', uselist=True,
        )


    def __init__(self, **kwargs):
        """Initialise un groupe d'hôtes."""
        super(HostGroup, self).__init__(**kwargs)

    def __unicode__(self):
        return u'%s - %s' % (self.groupname, self.hostname)
