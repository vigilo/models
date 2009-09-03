# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Service"""
from __future__ import absolute_import

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.types import UnicodeText
from sqlalchemy.orm import relation
from sqlalchemy.ext.associationproxy import association_proxy

from .vigilo_bdd_config import bdd_basename, DeclarativeBase, metadata

__all__ = ('Service', )

class Service(DeclarativeBase):

    __tablename__ = bdd_basename + 'service'

    name = Column(
        UnicodeText(),
        index=True, primary_key=True, nullable=False)
    type = Column(
        UnicodeText(),
        default=0,
        nullable=False)
    command = Column(
        UnicodeText(),
        default='',
        nullable=False)

    groups = association_proxy('service_groups', 'groups')


    def __init__(self, **kwargs):
        DeclarativeBase.__init__(self, **kwargs)


