# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table ApplicationLog"""

from __future__ import absolute_import

from sqlalchemy import Column
from sqlalchemy.types import Integer, DateTime, UnicodeText, Unicode
from sqlalchemy.exc import InvalidRequestError, IntegrityError
from datetime import datetime
import transaction

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .session import DBSession

__all__ = ('ApplicationLog', )

def l_(msg):
    """Stub pour la fonction d'i18n."""
    return unicode(msg)

class ApplicationLog(DeclarativeBase, object):
    """
    Mémorise les connexions/déconnexions des utilisateurs.
    
    @ivar idlog: Identifiant auto-généré de l'entrée.
    @ivar username: Nom de l'utilisateur à l'origine de l'événement.
    @ivar application: Nom de l'application dans lequel l'événement a eu lieu.
    @ivar timestamp: Horodateur indiquant à quel moment a eu lieu l'événement
        enregistré.
    @ivar message: Message décrivant le type d'événement enregistré.
    @ivar ip: Adresse IP de l'utilisateur lorsque l'événement a été enregistré.
    """

    __tablename__ = bdd_basename + "application_log"

    idlog = Column(
        Integer,
        primary_key=True, autoincrement=True, nullable=False,
    )

    username = Column(
        Unicode(255),
        nullable=False,
    )

    application = Column(
        Unicode(20),
        nullable=True,
    )

    timestamp = Column(
        DateTime(timezone=False),
        default=datetime.now(),
        nullable=False,
    )

    message = Column(
        UnicodeText,
        nullable=False,
    )

    ip = Column(
        Unicode(40),
        nullable=True,
    )


    def __init__(self, **kwargs):
        """Initialise une entrée des logs des accès."""
        super(ApplicationLog, self).__init__(**kwargs)

    @classmethod
    def add_login(cls, username, ip, application):
        """
        Enregistre une déconnexion.

        @param cls: La classe qui servira à enregistrer la connexion.
        @type cls: C{class}
        @param username: Le nom de l'utilisateur qui se connecte.
        @type username: C{str}
        @param ip: L'adresse IP (v4 ou v6) de cet utilisateur.
        @type ip: C{str} ou C{None}
        @param application: Le nom de l'application dans laquelle
            la connexion survient.
        """

        message = l_("User logged in.")
        if not ip is None:
            ip = u'' + ip
        log = cls(
            timestamp=datetime.now(),
            message=message,
            username=username,
            application=application,
            ip=ip,
        )
        DBSession.add(log)
        try:
            DBSession.flush()
        except (InvalidRequestError, IntegrityError):
            # XXX log error before we pass.
            pass

    @classmethod
    def add_logout(cls, username, ip, application):
        """
        Enregistre une déconnexion.

        @param cls: La classe qui servira à enregistrer la déconnexion.
        @type cls: C{class}
        @param username: Le nom de l'utilisateur qui se déconnecte.
        @type username: C{str}
        @param ip: L'adresse IP (v4 ou v6) de cet utilisateur.
        @type ip: C{str} ou C{None}
        @param application: Le nom de l'application dans laquelle
            la déconnexion survient.
        """

        message = l_("User logged out.")
        if not ip is None:
            ip = u'' + ip
        log = cls(
            timestamp=datetime.now(),
            message=message,
            username=username,
            application=application,
            ip=ip,
        )
        DBSession.add(log)
        try:
            DBSession.flush()
        except (InvalidRequestError, IntegrityError):
            # XXX log error before we pass.
            pass

