# vim: set fileencoding=utf-8 sw=4 ts=4 et :
"""
Gère les sessions d'accès à la BDD utilisées par les différents
composants de Vigilo.

On dispose de 2 types de session :

-   DBSession correspond à une session utilisant l'extension
    ZopeTransactionExtension. Il s'agit du type de session à utiliser de
    préférence dans les applications TurboGears. L'extension utilisée permet
    de faire un COMMIT des transactions automatiquement à la fin des requêtes
    HTTP (lorsque la requête a pu être traitée correctement, c'est-à-dire
    lorsque le code de retour vaut 200).

    Après discussion interne, on utilisera DBSession également dans les
    autres composants (corrélateur, ...), même si ces composants n'ont pas
    besoin des fonctionnalités apportées par ZopeTransactionExtension.
"""

from sqlalchemy.engine import engine_from_config
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

from vigilo.common.conf import settings

__all__ = ('DBSession', )

# ZTE session.
# We must go through transaction (a zodb extraction) to commit, rollback.
# There's also a session context to hold managed data, and the
# ZopeTransactionExtension makes that mostly transparent.
# The ZopeTransactionExtension prevents us
# from committing, etc, the session directly.
DBSession = scoped_session(sessionmaker(autoflush=True, autocommit=False,
                extension=ZopeTransactionExtension()))
DBSession.bind = engine_from_config(settings['VIGILO_SQLALCHEMY'], prefix='')
