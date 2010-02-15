# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table HostApplication."""
from sqlalchemy import Column
from sqlalchemy.types import Unicode, Integer
from sqlalchemy.orm import relation

from vigilo.models.configure import DeclarativeBase, ForeignKey
from vigilo.models.application import Application
from vigilo.models.vigiloserver import VigiloServer

__all__ = ('Installation', )

class Installation(DeclarativeBase):
    """
    Étant donné un serveur Vigilo et une application,
    cette table fournit l'identifiant Jabber à utiliser
    pour communiquer avec l'application hébergée sur
    ce serveur.

    @ivar idvigiloserver: Identifiant du serveur Vigilo.
    @ivar vigiloserver: Instance de L{VigiloServer}.
    @ivar idapp: Identifiant de l'application.
    @ivar application: Instance de l'L{Application}.
    @ivar jid: Identifiant Jabber (JID) à utiliser pour communiquer
        avec l'application via le bus XMPP.
    """
    __tablename__ = 'hostapp'

    idvigiloserver = Column(
        Integer,
        ForeignKey(
            VigiloServer.idvigiloserver,
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
            Application.idapp,
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

