# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table HostGroups"""
from __future__ import absolute_import

from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import UnicodeText

from .vigilo_bdd_config import bdd_basename, DeclarativeBase


class HostGroups(DeclarativeBase):

    __tablename__ = bdd_basename + 'hostgroups'

    hostname = Column(
        UnicodeText(),
        ForeignKey(bdd_basename + u'host.name'),
        primary_key=True, nullable=False)
    groupname = Column(
        UnicodeText(),
        ForeignKey(bdd_basename + u'groups.name'),
        index=True ,primary_key=True, nullable=False)


