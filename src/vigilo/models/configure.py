# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 sw=4 ts=4 et :
"""
Gère la session d'accès à la BDD utilisée par les différents
composants de Vigilo.

La session déclarée ici utilise l'extension ZopeTransactionExtension,
ce qui lui permet, dans le contexte de Turbogears, d'effectuer un COMMIT
automatiquement lorsqu'une requête HTTP a été traitée avec succès.

Après discussion en interne, on utilisera DBSession également dans les
composants qui ne sont pas liés à Turbogears (corrélateur, ...), et ce,
même si ces composants n'ont pas besoin des fonctionnalités apportées
par ZopeTransactionExtension.
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

__all__ = ('DBSession', 'metadata', 'DeclarativeBase', 'configure_db')

DeclarativeBase = declarative_base()
metadata = DeclarativeBase.metadata
DBSession = scoped_session(sessionmaker(autoflush=True, autocommit=False,
                extension=ZopeTransactionExtension()))
db_basename = ''

def configure_db(config_obj, prefix):
    from sqlalchemy.engine import engine_from_config

    # ZTE session.
    # We must go through transaction (a zodb extraction) to commit, rollback.
    # There's also a session context to hold managed data, and the
    # ZopeTransactionExtension makes that mostly transparent.
    # The ZopeTransactionExtension prevents us
    # from committing, etc, the session directly.
    engine = engine_from_config(config_obj, prefix=prefix)
    DBSession.configure(bind=engine)
    metadata.bind = DBSession.bind
    return engine

