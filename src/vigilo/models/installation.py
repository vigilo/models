# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table HostApplication."""
from __future__ import absolute_import

from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Unicode, Integer
from sqlalchemy.orm import relation

from .vigilo_bdd_config import bdd_basename, DeclarativeBase

__all__ = ('Installation', )

class Installation(DeclarativeBase):
    """
    Etant donné un serveur Vigilo et une application,
    cette table fournit l'identifiant Jabber à utiliser
    pour communiquer avec l'application hébergée sur
    ce serveur.
    """
    __tablename__ = bdd_basename + 'hostapp'

    idvigiloserver = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'vigiloserver.idvigiloserver',
            onupdate="CASCADE", ondelete="CASCADE",
        ),
        index=True,
        primary_key=True,
        autoincrement=False,
    )

    vigiloserver = relation('VigiloServer')

    idapp = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'application.idapp',
            onupdate='CASCADE', ondelete='CASCADE',
        ),
        primary_key=True,
        index=True,
        autoincrement=False,
    )

    application = relation('Application')

    jid = Column(
        Unicode(255),
        nullable=False,
    )

    def __init__(self, **kwargs):
        """Initialise une instance de HostBusApplication."""
        if 'jid' not in kwargs:
            raise KeyError, 'Missing value for "jid" attribute.'
        super(Installation, self).__init__(**kwargs)

