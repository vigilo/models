# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table ServiceTopo"""
from __future__ import absolute_import

from sqlalchemy.orm import mapper
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import UnicodeText

from .vigilo_bdd_config import bdd_basename, DeclarativeBase


class ServiceTopo(DeclarativeBase):

    __tablename__ = bdd_basename + 'servicetopo'

    servicename = Column(
        UnicodeText(),
        ForeignKey(bdd_basename + \
                u'service.name'),
        primary_key=True, nullable=False)

    function = Column(
        UnicodeText(),
        default='',
        nullable=False)
