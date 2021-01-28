# -*- coding: utf-8 -*-
# Copyright (C) 2006-2021 CS GROUP - France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèle pour la table Ventilation."""
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer
from sqlalchemy.orm import relation

from vigilo.models.session import DeclarativeBase
from vigilo.models.tables.host import Host
from vigilo.models.tables.vigiloserver import VigiloServer
from vigilo.models.tables.application import Application

__all__ = ('Ventilation', )

class Ventilation(DeclarativeBase, object):
    """
    Gestion de la ventilation des hôtes supervisés, c'est-à-dire que cette
    classe gère la répartition des hosts par serveur Vigilo et par groupe
    d'applications.

    @ivar idhost: Identifiant de l'hôte à ventiler.
    @ivar host: Instance de l'hôte à ventiler.
    @ivar idvigiloserver: Identifiant du serveur Vigilo sur lequel
        l'hôte sera ventilé.
    @ivar vigiloserver: Instance du serveur Vigilo sur lequel l'hôte
        sera ventilé.
    @ivar idapp: Identifiant de l'L{Application} installée.
    @ivar application: Instance de l'L{Application} installée.
    """

    __tablename__ = 'vigilo_ventilation'

    idhost = Column(
        Integer,
        ForeignKey(
            Host.idhost,
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=True,
            initially='IMMEDIATE',
        ),
        index=True,
        primary_key=True,
        autoincrement=False,
    )

    host = relation('Host')

    idvigiloserver = Column(
        Integer,
        ForeignKey(
            VigiloServer.idvigiloserver,
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=True,
            initially='IMMEDIATE',
        ),
        index=True,
        primary_key=True,
        autoincrement=False,
    )

    vigiloserver = relation('VigiloServer')

    idapp = Column(
        Integer,
        ForeignKey(
            Application.idapp,
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=True,
            initially='IMMEDIATE',
        ),
        index=True,
        primary_key=True,
        autoincrement=False,
    )

    application = relation('Application')

    def __init__(self, **kwargs):
        """Initialise une association ventilation."""
        super(Ventilation, self).__init__(**kwargs)

