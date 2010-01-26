# -*- coding: utf-8 -*-
"""Modèle pour la table Ventilation."""
from __future__ import absolute_import

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Unicode, Integer
from sqlalchemy.orm import relation, backref

from vigilo.models.vigilo_bdd_config import bdd_basename, DeclarativeBase

__all__ = ('CustomGraphView', )

class Ventilation(DeclarativeBase, object):
    """
    Modèle Ventilation spécifiant la répartition des hosts
    par serveur Vigilo et par groupe d'applications.
    """
    
    __tablename__ = bdd_basename + 'ventilation'

    idhost = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'host.idhost',
            onupdate="CASCADE", ondelete="CASCADE"),
        index=True,
        primary_key=True,
        autoincrement=False,
    )

    host = relation('Host')

    idvigiloserver = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'vigiloserver.idvigiloserver',
            onupdate="CASCADE", ondelete="CASCADE"),
        index=True,
        primary_key=True,
        autoincrement=False,
    )

    vigiloserver = relation('VigiloServer')

    idapp = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'application.idapp',
            onupdate="CASCADE", ondelete="CASCADE"),
        index=True,
        primary_key=True,
        autoincrement=False,
    )

    application = relation('Application')

    def __init__(self, **kwargs):
        """Initialise une association ventilation."""   
        super(Ventilation, self).__init__(**kwargs)

