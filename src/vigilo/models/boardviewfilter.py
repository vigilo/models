# -*- coding: utf-8 -*-
"""Modèle pour la table BoardViewFilter."""
from __future__ import absolute_import

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Unicode, UnicodeText

from vigilo.models.vigilo_bdd_config import bdd_basename, DeclarativeBase
from vigilo.models.session import DBSession

__all__ = ('BoardViewFilter', )

class BoardViewFilter(DeclarativeBase, object):
    """Gère les filtres personnalisés d'un utilisateur dans Vigiboard."""

    __tablename__ = bdd_basename + 'boardviewfilter'

    filtername = Column(
        Unicode(255),
        primary_key=True, index=True, nullable=False)

    username = Column(
        Unicode(255),
        ForeignKey(
            bdd_basename + 'user.user_name',
            onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True, index=True, nullable=False)

    hostname = Column(
        UnicodeText,
        ForeignKey(
            bdd_basename + 'host.name',
            onupdate="CASCADE", ondelete="CASCADE"),
        index=True, nullable=False)

    servicename = Column(
        UnicodeText,
        ForeignKey(
            bdd_basename + 'service.name',
            onupdate="CASCADE", ondelete="CASCADE"),
        index=True, nullable=False)

    message = Column(UnicodeText)

    trouble_ticket = Column(UnicodeText)

    def __init__(self, **kwargs):
        """Initialise un filtre."""
        super(BoardViewFilter, self).__init__(**kwargs)

