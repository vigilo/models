# -*- coding: utf-8 -*-
# Copyright (C) 2006-2012 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Script permettant de purger périodiquement la base de données
des événements associés à VigiBoard.
"""

import sys
import time
from datetime import datetime

from optparse import OptionParser
from sqlalchemy.engine.url import make_url
import sqlalchemy.sql.functions as sqlfuncs
from sqlalchemy import types as sqltypes
import transaction

from vigilo.common.gettext import translate, translate_narrow
_ = translate(__name__)
N_ = translate_narrow(__name__)

__all__ = (
    'main',
)

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


def clean_vigiboard(logger, options, url):
    """
    Cette fonction supprime les événements les plus anciens et
    correspondant à des agrégats fermés des tables utilisées
    par VigiBoard.

    @param logger: Logger à utiliser pour afficher des messages.
    @type logger: C{logging.Logger}
    @param options: Liste d'options demandées par l'utilisateur
        du script.
    @type options: C{optparse.Values}
    @param url: Adresse de la base de données, sous la forme d'une URL
        déjà pré-traitée par SQLAlchemy.
    @type url: C{sqlalchemy.engine.url.URL}
    """
    from vigilo.models.session import DBSession
    from vigilo.models.tables import Event, CorrEvent, StateName, HLSHistory

    sought_states = [
        StateName.statename_to_value(u'OK'),
        StateName.statename_to_value(u'UP'),
    ]

    if options.days is not None:
        if options.days >= 0:
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
                ).filter(Event.current_state.in_(sought_states)
                ).filter(CorrEvent.ack == CorrEvent.ACK_CLOSED
                ).filter(CorrEvent.timestamp_active <= old_date).all()
            ids = [event.idevent for event in ids]
            nb_deleted = DBSession.query(Event
                            ).filter(Event.idevent.in_(ids)
                            ).delete(synchronize_session='fetch')
            logger.info(_("Deleted %(nb_deleted)d closed events which were "
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
                            ).delete(synchronize_session='fetch')
            logger.info(_("Deleted %(nb_deleted)d entries in the history "
                        "for high level services which were at least "
                        "%(days)d days old.") % {
                            'nb_deleted': nb_deleted,
                            'days': options.days,
                        })

    if options.size is not None:
        if options.size >= 0:
            # Calcule la taille actuelle de la base de données Vigilo.
            dbsize = DBSession.query(pg_database_size(url.database)).scalar()

            if dbsize > options.size:
                logger.info(_("The database is %(size)d bytes big, which is "
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
                    ).filter(Event.current_state.in_(sought_states)
                    ).filter(CorrEvent.ack == CorrEvent.ACK_CLOSED
                    ).order_by(CorrEvent.timestamp_active.asc()).scalar()

                # Il n'y a plus aucun événement corrélé pouvant être supprimé.
                if idevent is None:
                    break

                nb_deleted = DBSession.query(Event
                                ).filter(Event.idevent == idevent
                                ).delete(synchronize_session='fetch')
                logger.info(_("Deleted closed event #%d to make room for "
                                "new events.") % idevent)
                if not nb_deleted:
                    break
                total_deleted += nb_deleted

                # On met à jour la taille connue de la base de données.
                dbsize = DBSession.query(
                            pg_database_size(url.database)
                        ).scalar()


            # Affiche quelques statistiques.
            logger.info(_("Deleted %(nb_deleted)d closed events. "
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

                # Il n'y a plus d'entrée d'historique concernant un service
                # de haut niveau pouvant être supprimée.
                if idhistory is None:
                    break

                nb_deleted = DBSession.query(HLSHistory
                                ).filter(HLSHistory.idhistory == idhistory
                                ).delete(synchronize_session='fetch')
                if not nb_deleted:
                    break
                total_deleted += nb_deleted

                # On met à jour la taille connue de la base de données.
                dbsize = DBSession.query(
                            pg_database_size(url.database)
                        ).scalar()

            # Affichage de statistiques actualisées.
            logger.info(_("Deleted %(nb_deleted)d history entries on "
                        "high level services. The database is now %(size)d "
                        "bytes big (limit: %(limit)d bytes)") % {
                            'nb_deleted': total_deleted,
                            'size': dbsize,
                            'limit': options.size,
                        })
    DBSession.flush()


def main(*args):
    """
    Point d'entrée du script qui supprime les événements
    obsolètes du bac à événements (VigiBoard).

    @note: Cette fonction ne rend pas la main, mais quitte
        l'exécution de Python à la fin de sa propre exécution.
        Les codes de retour possibles pour le script sont :
        * 0 : pas d'erreur
        * 1 : exception levée durant l'exécution
        * 2 : paramètres / options incorrects pour le script
    """
    parser = OptionParser()
    parser.add_option("-d", "--days", action="store", dest="days",
        type="int", default=None, help=_("Remove closed events which are "
        "at least DAYS old. DAYS must be a positive non-zero integer."))
    parser.add_option("-s", "--size", action="store", dest="size",
        type="int", default=None, help=_("Remove closed events, starting "
        "with the oldest ones, when the Vigilo database starts occupying "
        "more then SIZE bytes. SIZE must be a positive non-zero integer."))
    parser.add_option("-c", "--config", action="store", dest="config",
        type="string", default=None, help=_("Load configuration from "
        "this file."))

    (options, args) = parser.parse_args()

    from vigilo.common.conf import settings
    if options.config:
        settings.load_file(options.config)
    else:
        settings.load_module(__name__)

    from vigilo.common.logging import get_logger
    logger = get_logger(__name__)

    if args:
        logger.error(_('Too many arguments'))
        sys.exit(2)

    from vigilo.models.configure import configure_db
    try:
        configure_db(settings['database'], 'sqlalchemy_')
    except KeyError:
        logger.error(_('No database configuration found'))
        sys.exit(2)

    url = make_url(settings['database']['sqlalchemy_url'])

    if options.days is None and options.size is None:
        parser.error(N_(
            "Either -d or -s must be used. "
            "See %s --help for more information.") % sys.argv[0])
        sys.exit(2)

    try:
        clean_vigiboard(logger, options, url)
        transaction.commit()
        sys.exit(0)
    except Exception: # pylint: disable-msg=W0703
        # W0703: Catch "Exception"
        logger.exception(_('Some error occurred:'))
        transaction.abort()
        sys.exit(1)
