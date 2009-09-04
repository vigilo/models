# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table HostGroups"""
from __future__ import absolute_import

from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Unicode
from sqlalchemy.orm import relation

from .vigilo_bdd_config import bdd_basename, DeclarativeBase


class HostGroups(DeclarativeBase, object):

    __tablename__ = bdd_basename + 'hostgroups'

    hostname = Column(
        Unicode(255),
        ForeignKey(bdd_basename + u'host.name'),
        primary_key=True, nullable=False,
        info={'rum': {'field': 'Text'}})

    groupname = Column(
        Unicode(255),
        ForeignKey(bdd_basename + u'groups.name'),
        primary_key=True, nullable=False,
        info={'rum': {'field': 'Text'}})


#    host = relation('Host', backref='host_groups')
#    group = relation('Groups', backref='hosts')

    def __init__(self, **kwargs):
        """Initialise un groupe d'hôtes."""
        DeclarativeBase.__init__(self, **kwargs)

