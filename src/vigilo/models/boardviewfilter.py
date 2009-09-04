# -*- coding: utf-8 -*-
"""Modèle pour la table BoardViewFilter."""

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Unicode, UnicodeText, Integer

from vigilo.models.vigilo_bdd_config import bdd_basename, DeclarativeBase
from vigilo.models.session import DBSession


__all__ = ('BoardViewFilter', )

class BoardViewFilter(DeclarativeBase, object):
    """Gère les filtres personnalisés d'un utilisateur dans Vigiboard."""

    __tablename__ = bdd_basename + 'boardviewfilter'

    idfilter = Column(
        Integer,
        primary_key=True)

    username = Column(
        Unicode(255),
        ForeignKey(
            bdd_basename + 'user.user_name',
            onupdate="CASCADE", ondelete="CASCADE"),
        index=True, nullable=False)

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

    output = Column(UnicodeText)

    trouble_ticket = Column(UnicodeText)

    def __init__(self, **kwargs):
        """Initialise un filtre."""
        DeclarativeBase.__init__(self, **kwargs)

