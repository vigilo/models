# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Version"""
from __future__ import absolute_import

from sqlalchemy import Column
from sqlalchemy.types import Integer, UnicodeText

from .vigilo_bdd_config import bdd_basename, DeclarativeBase



class Version(DeclarativeBase):
    __tablename__ = bdd_basename + 'version'

    name = Column(
            UnicodeText(),
            index=True,primary_key=True, nullable=False)
    version = Column(
            UnicodeText(),
            nullable=False)


