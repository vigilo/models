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

from sqlalchemy import ForeignKey as SaForeignKey, \
                        ForeignKeyConstraint as SaForeignKeyConstraint
from sqlalchemy import Table as SaTable
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

from sqlalchemy.orm.scoping import ScopedSession
from sqlalchemy.schema import DDL, _bind_or_error
from sqlalchemy.sql import expression

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

class ForeignKeyConstraint(SaForeignKeyConstraint):
    """
    Une redéfinition des clés étrangères de SQLAlchemy
    qui ajoute automatiquement le préfixe des tables de
    Vigilo lorsque cela est nécessaire.
    """

    def __init__(self, columns, refcolumns, name=None, *args, **kwargs):
        """
        Instancie la ForeignKey en ajoutant le préfixe
        des tables de Vigilo.
        """
        if isinstance(name, basestring):
            name = configure.DB_BASENAME + name
        super(ForeignKeyConstraint, self).__init__(
            columns, refcolumns, name, *args, **kwargs)

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

class ClusteredDDL(DDL):
    def __init__(self, statement, cluster_name, cluster_sets, context=None, bind=None):
        # Si plusieurs instructions ont été passées (liste),
        # on les combine ici.
        if isinstance(statement, list):
            statement = ';'.join(statement)
        super(ClusteredDDL, self).__init__(statement, 'postgres', context, bind)
        self.cluster_name = cluster_name
        self.cluster_sets = cluster_sets

    def execute(self, bind=None, schema_item=None):
        if bind is None:
            bind = _bind_or_error(self)

        if self._should_execute(None, schema_item, bind):
            # On évalue le contexte une fois pour toute (il ne changera plus).
            context = self._prepare_context(schema_item, bind)
            cluster_name = '_' + self.cluster_name

            # Dans le cas où une réplication est en place,
            # on doit préparer le cluster pour le DDL.
            if self.cluster_sets and self.cluster_name:
                # On prépare le set du cluster, uniquement s'il est présent
                # (d'où la recherche sur set_id dans sl_set) et si son origine
                # (set_origin) correspond bien au nœud courant du cluster
                # (getlocalnodeid).
                prepare_statement = \
                    "SELECT %%(cluster_name)s." \
                        "ddlscript_prepare(:cluster_set,-1) " \
                    "FROM %%(cluster_name)s.sl_set " \
                    "WHERE set_origin = %%(cluster_name)s." \
                        "getlocalnodeid('%%(cluster_name)s') " \
                    "AND set_id =  :cluster_set;"
                executable = expression.text(prepare_statement % context % {
                    'cluster_name': cluster_name
                })
                for cluster_set in self.cluster_sets:
                    bind.execute(executable, params={
                        'cluster_set': int(cluster_set),
                    })

            # Exécution locale du DDL.
            statement = self._expand(schema_item, bind)
            res = bind.execute(expression.text(statement))

            # Propagation du DDL aux autres nœuds.
            if self.cluster_sets and self.cluster_name:
                # On prépare le DDL sur les sets présents tels que l'origine
                # (set_origin) correspond bien au nœud courant du cluster
                # (getlocalnodeid).
                repl_statement = \
                    "SELECT %%(cluster_name)s." \
                        "ddlscript_complete(:cluster_set,:statement,-1)" \
                    "FROM %%(cluster_name)s.sl_set " \
                    "WHERE set_origin = %%(cluster_name)s." \
                        "getlocalnodeid('%%(cluster_name)s') " \
                    "AND set_id =  :cluster_set;"
                executable = expression.text(repl_statement %
                    self._prepare_context(schema_item, bind) % {
                        'cluster_name': cluster_name,
                    })
                for cluster_set in self.cluster_sets:
                    bind.execute(executable, params={
                        'cluster_set': int(cluster_set),
                        'statement': statement,
                    })

            return res

    def _should_execute(self, event, schema_item, bind):
        # Permet de gérer une session donnée en argument.
        if isinstance(bind, ScopedSession):
            bind = bind.bind
        return super(ClusteredDDL, self)._should_execute(event, schema_item, bind)

    def _prepare_context(self, schema_item, bind):
        # Permet de gérer une session donnée en argument.
        if isinstance(bind, ScopedSession):
            bind = bind.bind
        return super(ClusteredDDL, self)._prepare_context(schema_item, bind)

DeclarativeBase = declarative_base(metaclass=PrefixedTables)
metadata = DeclarativeBase.metadata
DBSession = scoped_session(sessionmaker(autoflush=True, autocommit=False,
                extension=ZopeTransactionExtension()))
