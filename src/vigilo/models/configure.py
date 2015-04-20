# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 sw=4 ts=4 et :
# Copyright (C) 2006-2015 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Module permettant de configurer l'accès à la base de données
en vue de l'utilisation des tables du modèle de Vigilo.
"""

__all__ = (
    'DB_BASENAME',
    'DEFAULT_LANG',
    'SCHEMES',
    'DEPRECATED_SCHEMES',
    'configure_db',
)

DB_BASENAME = ''
DEFAULT_LANG = None
SCHEMES = None
DEPRECATED_SCHEMES = None

def configure_db(config_obj, prefix, db_basename=None):
    """
    Permet de configurer la base de données.

    @param config_obj: Objet contenant la configuration.
    @type config_obj: C{ConfigObj} ou C{PylonsConfig}
    @param prefix: Préfixe des paramètres de configuration
        liés à la base de données.
    @type prefix: C{basestring}
    @param db_basename: Préfixe des noms de tables de Vigilo.
    @type db_basename: C{basestring}
    @return: L'Engine configuré, utilisable par SQLAlchemy.
    @note: Le paramètre L{db_basename} N'EST PLUS utilisé.
        À la place, la valeur de la clé "db_basename" dans
        config_obj est automatiquement utilisée.
    """
    if db_basename is not None:
        import warnings
        warnings.warn(DeprecationWarning(
            'Passing a third argument to configure_db() is now deprecated.'
        ))

    # Permet de déterminer si l'objet config_obj est une configuration
    # de TurboGears (Pylons) ou bien un objet ConfigObj plus standard.
    using_tg = False
    try:
        from config import ConfigObj
    except ImportError:
        using_tg = True
    else:
        using_tg = (not isinstance(config_obj, ConfigObj))

    # Paramétrage du modèle. Doit être fait en tout premier.
    # vigilo.models.session dépend de cette initialisation.
    # pylint: disable-msg=W0603
    # W0603: Using the global statement
    global DB_BASENAME, DEFAULT_LANG, SCHEMES, DEPRECATED_SCHEMES

    # Préfixe des noms de tables.
    DB_BASENAME = config_obj.get('db_basename', '')

    # Langue par défaut des utilisateurs.
    DEFAULT_LANG = config_obj.get('lang', None)

    # Algorithmes de hachage des mots de passe.
    DEPRECATED_SCHEMES = \
        filter(None, config_obj.get('deprecated_password_schemes').split(' '))
    SCHEMES = filter(None, config_obj.get('password_schemes').split(' ')) + \
                DEPRECATED_SCHEMES

    import vigilo.models.session as session

    # Si la connexion à la base de données est déjà configurée,
    # on se contente de renvoyer l'objet déjà configuré.
    if session.metadata.bind is not None:
        return session.metadata.bind

    # ZTE session.
    # We must go through transaction (a zodb extraction) to commit, rollback.
    # There's also a session context to hold managed data, and the
    # ZopeTransactionExtension makes that mostly transparent.
    # The ZopeTransactionExtension prevents us
    # from committing, etc, the session directly.
    from sqlalchemy.engine import engine_from_config
    engine = engine_from_config(config_obj, prefix=prefix)

    session.DBSession.configure(bind=engine)
    session.metadata.bind = session.DBSession.bind
    return engine
