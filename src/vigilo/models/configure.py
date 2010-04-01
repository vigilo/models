# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 sw=4 ts=4 et :
"""
Module permettant de configurer l'accès à la base de données
en vue de l'utilisation des tables du modèle de Vigilo.
"""

__all__ = (
    'DB_BASENAME',
    'configure_db',
)

DB_BASENAME = ''

def configure_db(config_obj, prefix, db_basename):
    """
    Permet de configurer la base de données.
    
    @param config_obj: Objet contenant la configuration.
    @type config_obj: C{ConfigObj}
    @param prefix: Préfixe des paramètres de configuration
        liés à la base de données.
    @type prefix: C{basestring}
    @return: L'Engine configuré, utilisable par SQLAlchemy.
    """

    # Doit être fait en tout premier.
    # vigilo.models.session dépend de l'initialisation de cette valeur.
    from vigilo.models import configure
    configure.DB_BASENAME = db_basename

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
    print "engine from config_db = %s" % id(engine)

    session.DBSession.configure(bind=engine)
    session.metadata.bind = session.DBSession.bind
    print "m.c: session had bind %s" % id(session.DBSession.bind)
    print "m.c: metadata had bind %s" % id(session.metadata.bind)
    return engine

