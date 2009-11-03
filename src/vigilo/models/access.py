# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Access"""

from __future__ import absolute_import

from sqlalchemy import Column
from sqlalchemy.types import Integer, DateTime, UnicodeText, Unicode
from sqlalchemy.exc import InvalidRequestError, IntegrityError
from datetime import datetime
import transaction

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .session import DBSession

__all__ = ('Access', )

class Access(DeclarativeBase, object):
    """Mémorise les connexions/déconnexions des utilisateurs."""

    __tablename__ = bdd_basename + "access"

    idaccess = Column(
        Integer,
        primary_key=True, autoincrement=True, nullable=False,
    )

    timestamp = Column(DateTime(timezone=False), default=datetime.now())

    message = Column(UnicodeText)

    ip = Column(Unicode(40))


    def __init__(self, **kwargs):
        """Initialise une entrée des logs des accès."""
        super(Access, self).__init__(**kwargs)

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

        message = u"User '%s' logged in (%s)." % (username, application)
        if not ip is None:
            ip = u'' + ip
        access = cls(
            timestamp=datetime.now(),
            message=message,
            ip=ip,
        )
        DBSession.add(access)
        try:
            DBSession.flush()
        except (InvalidRequestError, IntegrityError):
            # XXX log error before we pass.
            pass
        else:
            transaction.commit()

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

        message = u"User '%s' logged out (%s)." % (username, application)
        if not ip is None:
            ip = u'' + ip
        access = cls(
            timestamp=datetime.now(),
            message=message,
            ip=ip,
        )
        DBSession.add(access)
        try:
            DBSession.flush()
        except (InvalidRequestError, IntegrityError):
            # XXX log error before we pass.
            pass
        else:
            transaction.commit()

