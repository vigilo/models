# -*- coding: utf-8 -*-
# Copyright (C) 2006-2020 CS GROUP - France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

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

from sqlalchemy import event as SaEvent
from sqlalchemy import exc as sa_exc
from sqlalchemy.orm import scoped_session, sessionmaker, query
from sqlalchemy.orm.scoping import ScopedSession
from sqlalchemy.schema import DDL as SaDDL
from sqlalchemy.sql import expression
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from zope.sqlalchemy import ZopeTransactionExtension

import vigilo.models.configure as configure

__all__ = (
    'DBSession',
    'metadata',
    'DeclarativeBase',
)

class MigrationDDL(SaDDL):
    """
    Exécute une requête SQL destinée à PostgreSQL
    et qui modifie le schéma (DDL).
    """
    def __init__(self, statement, context=None, bind=None):
        """
        Initialisation.

        @param statement: Une requête SQL ou une liste de requêtes SQL.
        @param statement: C{basestr} ou C{list} de C{basestr}
        @param context: Valeurs contextuelles de substitution.
        @type context: C{dict}
        @param bind: Connexion à la base de données maître.
        @type bind: C{Connectable}
        """
        # Si plusieurs instructions ont été passées (liste),
        # on les combine ici.
        if isinstance(statement, list):
            statement = ';'.join(statement)
        # Initialement, les migrations étaient spécifiques à PostgreSQL.
        # Cette contrainte est désormais levée et le script s'applique
        # quel que soit le dialecte (d'où l'argument None ci-dessous).
        super(MigrationDDL, self).__init__(statement, None, context, bind)

    def execute(self, bind=None, schema_item=None):
        """
        Exécute la requête ou la série de requêtes associées
        à cet objet.

        @param bind: Connexion à la base de données maître.
        @type bind: C{Connectable}
        @param schema_item: Élément du modèle sur lequel
            porte la modification.
        @type schema_item: C{Table}
        @return: Résultat de l'exécution de la requête sur
            le nœud maître.
        @rtype: C{ResultProxy}
        """
        if self._should_execute(None, schema_item, bind):
            return bind.execute(self.against(schema_item))

    def _should_execute(self, event, schema_item, bind):
        """
        Détermine si le DDL doit être exécuté ou non.
        """
        # Permet de gérer une session donnée en argument.
        if isinstance(bind, ScopedSession):
            bind = bind.bind
        return super(MigrationDDL, self)._should_execute(schema_item, bind)

    def _prepare_context(self, schema_item, bind):
        """
        Prépare le contexte de substitution.
        """
        # Permet de gérer une session donnée en argument.
        if isinstance(bind, ScopedSession):
            bind = bind.bind
        return super(MigrationDDL, self)._prepare_context(schema_item, bind)

def DDL(statement, when=None, obj=None, bind=None, dialect=None, context=None):
    """
    Construit un objet de type DDL en utilisant l'API
    correspondant à la version de SQLAlchemy en cours
    d'utilisation.

    Cette fonction peut être utilisée pour exécuter
    une commande SQL de deux manières distinctes.
    -   Soit lorsqu'un événement se produit (par exemple,
        lors de la création d'une certaine table du modèle),
        en passant les paramètres when et obj.
    -   Soit immédiatement en ne passant que le paramètre bind.
    Ces deux cas d'usage sont mutuellement exclusifs.

    @param statement: Commande SQL à exécuter touchant au
        schéma de la base (et donc, utilisant le DDL).
    @type statement: C{str}
    @param when: Nom de l'événement à attendre pour exécuter
        le DDL, par exemple "before-create".
    @type when: C{str}
    @param obj: Objet support du DDL à exécuter (généralement
        une Table).
    @param bind: Connexion à la base de données (Session ou Metadata),
        dans le cas où le DDL doit être exécuté immédiatement.
    @param dialect: Nom d'un dialecte SQL supporté par SQLAlchemy.
        Le DDL ne sera exécuté que si le dialecte utilisé par la
        base de données correspond à donné ici.
    @type dialect: C{str}
    @param context: Contexte qui sera passé au DDL (interpolé)
        au moment de son exécution.
    @type context: C{dict}
    """
    # 2 cas d'utilisation exclusifs :
    # - soit lorsqu'un événement se produit
    # - soit en exécution immédiate
    assert (bind is None or when is not None) or \
           (bind is not None or when is None)
    if context is None:
        context = {}

    ddl = SaDDL(statement, context=context)
    if when is None:
        ddl.execute(bind)
    else:
        # Les mots dans le nom de l'événement sont séparés par
        # des '_' dans cette version de SQLAlchemy.
        SaEvent.listen(obj, when.replace('-', '_'),
                     ddl.execute_if(dialect=dialect))

class Query(query.Query):
    """
    Une extension de la classe de requête par défaut de SQLAlchemy
    qui ajoute le support des constructions "SELECT DISTINCT ON (...) ..."
    de PostgreSQL (backport de SQLAlchemy 0.7).
    Cf. http://www.sqlalchemy.org/trac/ticket/1069
    et  http://www.sqlalchemy.org/trac/changeset/a7f581395db1/
    """
    def _no_statement_condition(self, meth):
        """
        Récopié depuis SQLAlchemy 0.5.6 avec des ajustements pour rester
        compatible avec SQLAlchemy 0.5.5. Nécessaire car la méthode était
        privée dans 0.5.5 et n'est devenue protégée que dans 0.5.6.
        """
        # self._enable_assertions n'existe que depuis SA 0.5.6.
        if not getattr(self, '_enable_assertions', True):
            return
        if self._statement:
            raise sa_exc.InvalidRequestError(
                ("Query.%s() being called on a Query with an existing full "
                 "statement - can't apply criterion.") % meth)


    @query._generative(_no_statement_condition) # pylint: disable-msg=W0212
    # W0212: Access to a protected member of a client class
    def distinct(self, *criterion):
        """
        X{Backport} depuis SQLAlchemy 0.7.
        Ajoute un ``DISTINCT`` à la requête et retourne la nouvelle
        ``Query`` ainsi créée.

        :param \*expr: expressions optionnels se rapportant à des colonnes
              et qui généreront une expression DISTINCT ON dans PostgreSQL.
        """
        # pylint: disable-msg=W0212
        # W0212: Access to a protected member of a client class
        if not criterion:
            self._distinct = True
        else:
            criterion = [
                self._adapt_clause(
                    expression._literal_as_text(o),
                    True, True)
                for o in criterion
            ]
            if isinstance(self._distinct, list):
                self._distinct += criterion
            else:
                self._distinct = criterion

DeclarativeBase = declarative_base()
metadata = DeclarativeBase.metadata
DBSession = scoped_session(sessionmaker(autoflush=True,
                                        autocommit=False,
                                        extension=ZopeTransactionExtension(),
                                        query_cls=Query))
