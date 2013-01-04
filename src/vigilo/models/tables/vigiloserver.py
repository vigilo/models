# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2013 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""VigiloServer model"""
from sqlalchemy import Column
from sqlalchemy.types import Integer, Unicode, Boolean

from vigilo.models.session import DeclarativeBase, DBSession

__all__ = ('VigiloServer', )

class VigiloServer(DeclarativeBase, object):
    """
    Cette classe gère les informations concernant un serveur sur lequel
    Vigilo est installé.

    @ivar idvigiloserver: Identifiant auto-généré du serveur.
    @ivar name: Nom complet (FQDN) du serveur hébergeant Vigilo.
    @ivar description: Une description intelligible du serveur.
    """
    __tablename__ = 'vigiloserver'


    idvigiloserver = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name = Column(
        Unicode(255),
        index=True,
        unique=True,
        nullable=False,
    )

    disabled =  Column(
        Boolean,
        default = False,
        nullable = False,
    )

    def __init__(self, **kwargs):
        """
        Initialise l'instance avec les informations du serveur.

        @param kwargs: Un dictionnaire avec les informations.
        @type kwargs: C{dict}
        """
        super(VigiloServer, self).__init__(**kwargs)

    def __unicode__(self):
        """
        Conversion en unicode.

        @return: Le nom du groupe.
        @rtype: C{unicode}
        """
        return self.name

    def __str__(self):
        return str(self.name)


    @classmethod
    def by_vigiloserver_name(cls, servername):
        """
        Renvoie le serveur dont le nom est L{servername}.

        @param cls: La classe à utiliser, c'est-à-dire L{VigiloServer}.
        @type cls: C{class}
        @param servername: Nom du serveur Vigilo à rechercher.
        @type servername: C{unicode}
        @return: Le serveur Vigilo demandé.
        @rtype: L{VigiloServer}
        """
        return DBSession.query(cls).filter(cls.name == servername).first()

