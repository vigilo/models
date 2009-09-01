# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Groups"""
from __future__ import absolute_import

from sqlalchemy import Column
from sqlalchemy.types import UnicodeText

from .vigilo_bdd_config import bdd_basename, DeclarativeBase



class Groups(DeclarativeBase):
    __tablename__ = bdd_basename + 'groups'

    name = Column(
        UnicodeText(),
        primary_key=True, nullable=False)
    parent = Column(
        UnicodeText(),
        index=True)

