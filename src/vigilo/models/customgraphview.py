# -*- coding: utf-8 -*-
"""Modèle pour la table CustomGraphView."""
from __future__ import absolute_import

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Unicode, Integer

from vigilo.models.vigilo_bdd_config import bdd_basename, DeclarativeBase

__all__ = ('CustomGraphView', )

class CustomGraphView(DeclarativeBase, object):
    """Gère les vues personnalisées d'un utilisateur dans Vigigraph."""

    __tablename__ = bdd_basename + 'customgraphview'

    viewname = Column(
        Unicode(255),
        primary_key=True)

    username = Column(
        Unicode(255),
        ForeignKey(
            bdd_basename + 'user.user_name',
            onupdate="CASCADE", ondelete="CASCADE"),
        index=True, nullable=False, primary_key=True)

    graphname = Column(
        Unicode(255),
        ForeignKey(
            bdd_basename + 'graph.name',
            onupdate="CASCADE", ondelete="CASCADE"),
        index=True, nullable=False, primary_key=True)

    hostname = Column(
        Unicode(255),
        ForeignKey(
            bdd_basename + 'host.name',
            onupdate="CASCADE", ondelete="CASCADE"),
        index=True, nullable=False, primary_key=True)

    pos_x = Column(
        Integer,
        nullable=False)

    pos_y = Column(
        Integer,
        nullable=False)

    def __init__(self, **kwargs):
        """Initialise une vue."""   
        super(CustomGraphView, self).__init__(**kwargs)

