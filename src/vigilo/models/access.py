# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Access"""

from __future__ import absolute_import

from sqlalchemy import Column
from sqlalchemy.types import Integer, DateTime, UnicodeText
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


    def __init__(self, **kwargs):
        """Initialise une entrée des logs des accès."""
        super(Access, self).__init__(**kwargs)

    @classmethod
    def add_login(cls, username, application):
        message = u"User '%s' logged in (%s)." % (username, application)
        access = cls(
            timestamp=datetime.now(),
            message=message,
        )
        DBSession.add(access)
        try:
            DBSession.flush()
        except:
            # XXX log error before we pass.
            pass
        else:
            transaction.commit()

    @classmethod
    def add_logout(cls, username, application):
        message = u"User '%s' logged out (%s)." % (username, application)
        access = cls(
            timestamp=datetime.now(),
            message=message,
        )
        DBSession.add(access)
        try:
            DBSession.flush()
        except:
            # XXX log error before we pass.
            pass
        else:
            transaction.commit()

