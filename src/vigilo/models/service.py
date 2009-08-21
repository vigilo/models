# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Service"""
from __future__ import absolute_import

from sqlalchemy.orm import mapper
from sqlalchemy import Table, Column
from sqlalchemy.types import UnicodeText

from .vigilo_bdd_config import bdd_basename, DeclarativeBase

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



