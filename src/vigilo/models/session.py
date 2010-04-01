# -*- coding: utf-8 -*-
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

import vigilo.models.configure as configure

__all__ = (
    'DBSession',
    'metadata',
    'DeclarativeBase',
    'Table',
    'ForeignKey',
)

class ForeignKey(SaForeignKey):
    """
    Une redéfinition des clés étrangères de SQLAlchemy
    qui ajoute automatiquement le préfixe des tables de
    Vigilo lorsque cela est nécessaire.
    """

    def __init__(self, name, *args, **kwargs):
        """
        Instancie la ForeignKey en ajoutant le préfixe
        des tables de Vigilo.
        """
        if isinstance(name, basestring):
            name = configure.DB_BASENAME + name
        super(ForeignKey, self).__init__(name, *args, **kwargs)

class Table(SaTable):
    """
    Une redéfinition de l'objet Table de SQLAlchemy
    qui ajoute automatiquement le préfixe des tables de
    Vigilo.
    """

    def __init__(self, name, *args, **kwargs):
        """
        Instancie la Table en ajoutant le préfixe
        des tables de Vigilo.
        """
        if isinstance(name, basestring):
            name = configure.DB_BASENAME + name
        super(Table, self).__init__(name, *args, **kwargs)

class PrefixedTables(DeclarativeMeta):
    """
    Une méta-classe qui permet de préfixer automatiquement
    le nom de toutes les tables de la base de données avec
    le préfixe configuré dans la configuration sous la clé
    C{db_basename}.
    """

    def __init__(mcs, classname, bases, dict_):
        """
        Permet l'ajout automatique du préfixe aux tables
        du modèle, lorsque celles-ci sont définies
        en utilisant le mode "Declarative" de SQLAlchemy.
        """
        if '__tablename__' in dict_:
            mcs.__tablename__ = dict_['__tablename__'] = \
                configure.DB_BASENAME + dict_['__tablename__']
        DeclarativeMeta.__init__(mcs, classname, bases, dict_)

DeclarativeBase = declarative_base(metaclass=PrefixedTables)
metadata = DeclarativeBase.metadata
DBSession = scoped_session(sessionmaker(autoflush=True, autocommit=False,
                extension=ZopeTransactionExtension()))

