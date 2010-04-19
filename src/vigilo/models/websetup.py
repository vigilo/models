# -*- coding: utf-8 -*-
"""Peuple la base de données."""

import sys
import time
import transaction
import sqlalchemy.sql.functions as sqlfuncs
from sqlalchemy import types as sqltypes

__all__ = ['populate_db', 'init_db']



def populate_db(bind):
    """Placez les commandes pour peupler la base de données ici."""
    import logging
    LOGGER = logging.getLogger(__name__)

    from vigilo.models.session import DBSession, metadata

    # Chargement du modèle.
    from vigilo.models import tables
    from vigilo.models import VIGILO_MODELS_VERSION

    # Création des tables
    print "Creating tables"
    metadata.create_all(bind=bind)

    # Création d'un jeu de données par défaut.
    print "Setting up the generic tables"
    manager = tables.User()
    manager.user_name = u'manager'
    manager.email = u'manager@somedomain.com'
    manager.fullname = u'Manager'
    manager.password = u'managepass'
    DBSession.add(manager)
    DBSession.flush()

    group = tables.UserGroup()
    group.group_name = u'managers'
    group.users.append(manager)
    DBSession.add(group)
    DBSession.flush()

    permission = tables.Permission()
    permission.permission_name = u'manage'
    permission.usergroups.append(group)
    DBSession.add(permission)
    DBSession.flush()

    editor = tables.User()
    editor.user_name = u'editor'
    editor.email = u'editor@somedomain.com'
    editor.fullname = u'Editor'
    editor.password = u'editpass'
    DBSession.add(editor)
    DBSession.flush()

    group = tables.UserGroup()
    group.group_name = u'editors'
    group.users.append(editor)
    DBSession.add(group)
    DBSession.flush()

    permission = tables.Permission()
    permission.permission_name = u'edit'
    permission.usergroups.append(group)
    DBSession.add(permission)
    DBSession.flush()

    version = tables.Version()
    version.name = u'vigilo.models'
    version.version = VIGILO_MODELS_VERSION
    DBSession.add(version)
    DBSession.flush()

    DBSession.add(tables.StateName(statename=u'OK', order=0))
    DBSession.add(tables.StateName(statename=u'UNKNOWN', order=1))
    DBSession.add(tables.StateName(statename=u'WARNING', order=2))
    DBSession.add(tables.StateName(statename=u'CRITICAL', order=3))
    DBSession.add(tables.StateName(statename=u'UP', order=0))
    DBSession.add(tables.StateName(statename=u'UNREACHABLE', order=1))
    DBSession.add(tables.StateName(statename=u'DOWN', order=3))
    DBSession.flush()

    # Spécifique projets
    from pkg_resources import working_set
    for entry in working_set.iter_entry_points("vigilo.models", "populate_db"):
        # Charge les tables spécifiques
        pop_db = entry.load()
        print "Setting up for %s" % entry.dist.project_name
        pop_db(bind)

    transaction.commit()
    print "Successfully setup"

def init_db():
    """
    Cette fonction est appelée par le script vigiboard-init-db
    pour initialiser la base de données de Vigiboard.
    """
    from vigilo.common.conf import settings
    settings.load_module(__name__)

    from vigilo.models.configure import configure_db
    engine = configure_db(settings['database'], 'sqlalchemy_',
        settings['database']['db_basename'])
    populate_db(engine)


class pg_database_size(sqlfuncs.GenericFunction):
    """
    Fonction permettant d'utiliser l'expression "pg_database_size"
    de PostgreSQL afin de déterminer la taille occupée sur le disque
    par la base de données.

    @note: Cette fonction est spécifique à PostgreSQL.
    """
    __return_type__ = sqltypes.Integer

    def __init__(self, arg, **kwargs):
        super(pg_database_size, self).__init__(args=[arg], **kwargs)

def clean_vigiboard(*args):
    """
    Cette fonction supprime les événements les plus anciens
    des tables utilisées par VigiBoard.
    """

    from datetime import datetime
    from optparse import OptionParser

    from vigilo.common.conf import settings
    settings.load_module(__name__)

    from vigilo.models.configure import configure_db
    configure_db(settings['database'], 'sqlalchemy_',
        settings['database']['db_basename'])

    from vigilo.common.logging import get_logger
    LOGGER = get_logger(__name__)

    from vigilo.common.gettext import translate
    _ = translate(__name__)

    from vigilo.models.session import DBSession
    from vigilo.models.tables import Event, CorrEvent, StateName, HLSHistory

    parser = OptionParser()
    parser.add_option("-d", "--days", action="store", dest="days",
        type="int", default=None, help=_("Remove closed events which are "
        "at least DAYS old. DAYS must be a positive non-zero integer."))
    parser.add_option("-s", "--size", action="store", dest="size",
        type="int", default=None, help=_("Remove closed events, starting "
        "with the oldest ones, when the Vigilo database starts occupying "
        "more then SIZE bytes. SIZE must be a positive non-zero integer."))

    (options, args) = parser.parse_args()

    if args:
        LOGGER.error(_('Too many arguments'))
        sys.exit(1)

    if options.days is None and options.size is None:
        parser.print_usage()
        sys.exit(1)

    if options.days is not None:
        if options.days > 0:
            # Génère une date qui se trouve options.days jours dans le passé.
            old_date = datetime.fromtimestamp(
                time.time() - options.days * 86400)

            # On supprime tous les événements dont l'idevent correspond à
            # un événement corrélé dont la dernière date d'activation est
            # plus vieille que old_date.
            # Comme les relations/FK sont créées en CASCADE, la suppression
            # des événements entraine aussi la suppression des événements
            # corrélés, des agrégats et de l'historique des événements.
            ids = DBSession.query(
                    Event.idevent
                ).join(
                    (CorrEvent, Event.idevent == CorrEvent.idcause)
                ).filter(StateName.statename.in_([u'OK', u'UP'])
                ).filter(CorrEvent.status == u'AAClosed'
                ).filter(CorrEvent.timestamp_active <= old_date).all()
            ids = [event.idevent for event in ids]
            nb_deleted = DBSession.query(Event).filter(
                            Event.idevent.in_(ids)).delete()
            LOGGER.info(_("Deleted %(nb_deleted)d closed events which were "
                            "at least %(days)d days old.") % {
                            'nb_deleted': nb_deleted,
                            'days': options.days,
                        })

            # On supprime les entrées d'historique concernant les changements
            # d'état des services de haut niveau qui ont été ajoutées avant
            # old_date.
            nb_deleted = DBSession.query(
                                HLSHistory
                            ).filter(HLSHistory.timestamp <= old_date
                            ).delete()
            LOGGER.info(_("Deleted %(nb_deleted)d entries in the history "
                        "for high level services which were at least "
                        "%(days)d days old.") % {
                            'nb_deleted': nb_deleted,
                            'days': options.days,
                        })

    if options.size is not None:
        if options.size > 0:
            # Calcule la taille actuelle de la base de données Vigilo.
            from sqlalchemy.engine.url import make_url
            url = make_url(settings['database']['sqlalchemy_url'])
            dbsize = DBSession.query(pg_database_size(url.database)).scalar()

            if dbsize > options.size:
                LOGGER.info(_("The database is %(size)d bytes big, which is "
                    "more than the limit (%(limit)d bytes). I will now delete "
                    "old closed events and history entries to make room for "
                    "new ones.") % {
                        'size': dbsize,
                        'limit': options.size,
                    })

            # On supprime les événements clos en commençant par
            # les plus anciens.
            total_deleted = 0
            while dbsize > options.size:
                idevent = DBSession.query(
                        Event.idevent
                    ).join(
                        (CorrEvent, Event.idevent == CorrEvent.idcause)
                    ).filter(StateName.statename.in_([u'OK', u'UP'])
                    ).filter(CorrEvent.status == u'AAClosed'
                    ).order_by(CorrEvent.timestamp_active.asc()).scalar()
                if idevent is None:
                    break

                nb_deleted = DBSession.query(Event).filter(
                                Event.idevent == idevent).delete()
                LOGGER.info(_("Deleted closed event #%d to make room for "
                                "new events.") % idevent)
                if not nb_deleted:
                    break
                total_deleted += nb_deleted

            # Affiche quelques statistiques.
            dbsize = DBSession.query(pg_database_size(url.database)).scalar()
            LOGGER.info(_("Deleted %(nb_deleted)d closed events. "
                "The database is now %(size)d bytes big (limit: "
                "%(limit)d bytes)") % {
                    'nb_deleted': total_deleted,
                    'size': dbsize,
                    'limit': options.size,
                })

            # On supprime les entrées d'historique concernant les changements
            # d'état des services de haut niveau, en commençant par les plus
            # anciens.
            total_deleted = 0
            while dbsize > options.size:
                idhistory = DBSession.query(HLSHistory.idhistory
                                ).order_by(HLSHistory.timestamp.asc()
                                ).scalar()
                if idhistory is None:
                    break

                nb_deleted = DBSession.query(HLSHistory).filter(
                                HLSHistory.idhistory == idhistory).delete()
                if not nb_deleted:
                    break
                total_deleted += nb_deleted

            # Affichage de statistiques actualisées.
            dbsize = DBSession.query(pg_database_size(url.database)).scalar()
            LOGGER.info(_("Deleted %(nb_deleted)d history entries on "
                        "high level services. The database is now %(size)d "
                        "bytes big (limit: %(limit)d bytes)") % {
                            'nb_deleted': total_deleted,
                            'size': dbsize,
                            'limit': options.size,
                        })

    transaction.commit()
    sys.exit(0)

