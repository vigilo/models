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

from sqlalchemy import ForeignKey as SaForeignKey
from sqlalchemy import Table as SaTable
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

__all__ = (
    'DBSession',
    'metadata',
    'DeclarativeBase',
    'configure_db',
    'Table',
    'ForeignKey',
)

def _get_basename():
    has_tg = False
    try:
        # On tente d'obtenir le préfixe à utiliser à partir
        # de la configuration de Turbogears.
        from tg import config
        if "db_basename" in config:
            has_tg = True
    except ImportError:
        has_tg = False

    if has_tg:
        return config["db_basename"]
    else:
        # Turbogears n'est pas disponible, on essaye
        # avec vigilo.common.conf.
        from vigilo.common.conf import settings
        return settings['database']['db_basename']


class ForeignKey(SaForeignKey):
    """
    Une redéfinition des clés étrangères de SQLAlchemy
    qui ajoute automatiquement le préfixe des tables de
    Vigilo lorsque cela est nécessaire.
    """

    def __init__(self, name, *args, **kwargs):
        if isinstance(name, basestring):
            name = _get_basename() + name
        super(ForeignKey, self).__init__(name, *args, **kwargs)

class Table(SaTable):
    """
    Une redéfinition de l'objet Table de SQLAlchemy
    qui ajoute automatiquement le préfixe des tables de
    Vigilo.
    """

    def __init__(self, name, *args, **kwargs):
        if isinstance(name, basestring):
            name = _get_basename() + name
        super(Table, self).__init__(name, *args, **kwargs)

class PrefixedTables(DeclarativeMeta):
    """
    Une méta-classe qui permet de préfixer automatiquement
    le nom de toutes les tables de la base de données avec
    le préfixe configuré dans la configuration sous la clé
    C{db_basename}.
    """

    def __init__(cls, classname, bases, dict_):
        if '__tablename__' in dict_:
            cls.__tablename__ = dict_['__tablename__'] = \
                _get_basename() + dict_['__tablename__']
        return DeclarativeMeta.__init__(cls, classname, bases, dict_)


def configure_db(config_obj, prefix):
    """Permet de configurer la base de données."""

    import sys
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


DeclarativeBase = declarative_base(metaclass=PrefixedTables)

metadata = DeclarativeBase.metadata
DBSession = scoped_session(sessionmaker(autoflush=True, autocommit=False,
                extension=ZopeTransactionExtension()))

