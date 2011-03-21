# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 sw=4 ts=4 et :
"""
Module permettant de configurer l'accès à la base de données
en vue de l'utilisation des tables du modèle de Vigilo.
"""

__all__ = (
    'DB_BASENAME',
    'DEFAULT_LANG',
    'HASHING_FUNC',
    'EXTERNAL_AUTH',
    'configure_db',
)

DB_BASENAME = ''
DEFAULT_LANG = None
HASHING_FUNC = None
EXTERNAL_AUTH = False

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
    global DB_BASENAME, DEFAULT_LANG, HASHING_FUNC, EXTERNAL_AUTH

    # Préfixe des noms de tables.
    DB_BASENAME = config_obj.get('db_basename', '')

    # Langue par défaut des utilisateurs.
    DEFAULT_LANG = config_obj.get('lang', None)

    # Fonction de hachage des mots de passe.
    HASHING_FUNC = config_obj.get(
        'password_hashing_function', None)

    # Utilisation ou non d'une authentification externe (ex: Kerberos).
    # Note de rétro-compatibilité : si la clé "external_auth" n'est
    # pas définie, on se rabat sur la clé "use_kerberos".
    if using_tg:
        from paste.deploy.converters import asbool
        external_auth = \
            'external_auth' in config_obj and config_obj['external_auth'] or \
            'use_kerberos' in config_obj and config_obj['use_kerberos'] or \
            None
        EXTERNAL_AUTH = asbool(external_auth)
    else:
        EXTERNAL_AUTH = \
            'external_auth' in config_obj and \
            config_obj.as_bool('external_auth') or \
            'use_kerberos' in config_obj and \
            config_obj.as_bool('use_kerberos') or \
            None

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
