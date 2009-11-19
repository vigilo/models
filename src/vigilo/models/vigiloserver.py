# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table VigiloServer"""
from __future__ import absolute_import

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Unicode, Integer
from sqlalchemy.orm import relation, backref

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .session import DBSession
from .secondary_tables import GROUP_PERMISSION_TABLE

__all__ = ('VigiloServer', )

class VigiloServer(DeclarativeBase, object):
    """Gère les serveurs de Vigilo."""
    __tablename__ = bdd_basename + 'vigiloserver'

    idsrv = Column(
            Integer,
            primary_key=True, 
            autoincrement=True,)

    fqdn = Column(
        Unicode(255),
        nullable=False)
