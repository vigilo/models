# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 sw=4 ts=4 et :
# Copyright (C) 2006-2020 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Script permettant de refermer automatiquement les événements
se trouvant dans l'état OK et/ou UP dans VigiBoard.
"""

import sys, os
import transaction
import time
from datetime import datetime
from optparse import OptionParser
import pwd # Disponible uniquement sur Unix-like

from vigilo.common.gettext import translate, translate_narrow
_ = translate(__name__)
N_ = translate_narrow(__name__)

__all__ = (
    'main',
)

def close_green(logger, options):
    """
    Cette fonction ferme les événements qui apparaissent
    en vert dans VigiBoard (c'est-à-dire ceux dans l'état
    "OK" ou "UP").

    @param logger: Logger à utiliser pour afficher des messages.
    @type logger: C{logging.Logger}
    @param options: Liste d'options demandées par l'utilisateur
        du script.
    @type options: C{optparse.Values}
    @return: Nombre d'événements qui ont été fermés automatiquement.
    @rtype: C{int}
    """
    from vigilo.models.session import DBSession
    from vigilo.models.tables import Event, CorrEvent, StateName, EventHistory

    sought_states = []
    if options.state_up:
        sought_states.append(StateName.statename_to_value(u'UP'))
    if options.state_ok:
        sought_states.append(StateName.statename_to_value(u'OK'))

    query = DBSession.query(
            CorrEvent
        ).join(
            (Event, Event.idevent == CorrEvent.idcause),
        ).filter(Event.current_state.in_(sought_states)
        ).filter(CorrEvent.ack != CorrEvent.ACK_CLOSED)
    if options.days is not None and options.days > 0:
        # Génère une date qui se trouve options.days jours dans le passé.
        old_date = datetime.utcfromtimestamp(time.time() - options.days * 86400)
        query = query.filter(Event.timestamp <= old_date)

    events = query.all()
    username = unicode(pwd.getpwuid(os.getuid())[0])
    for event in events:
        logger.info(_('closing event on %s') % event.cause.supitem)

        # On ajoute un message dans l'historique pour la traçabilité.
        history = EventHistory(
                type_action=u"Acknowledgement change state",
                idevent=event.idcause,
                value=u"",
                text=u"Automatically marked the event as closed",
                username=username,
                timestamp=datetime.utcnow(),
            )
        DBSession.add(history)

        # On referme l'événement.
        event.ack = CorrEvent.ACK_CLOSED
        DBSession.flush()
    return len(events)


def main(*args):
    """
    Point d'entrée du script qui ferme les événements en vert
    dans le bac à événements (VigiBoard).

    @note: Cette fonction ne rend pas la main, mais quitte
        l'exécution de Python à la fin de sa propre exécution.
        Les codes de retour possibles pour le script sont :
        * 0 : pas d'erreur
        * 1 : exception levée durant l'exécution
        * 2 : paramètres / options incorrects pour le script
    """
    parser = OptionParser()
    parser.add_option("-d", "--days", action="store", dest="days",
        type="int", default=None, help=_("Close events which are "
        "at least DAYS old. DAYS must be a positive non-zero integer."))
    parser.add_option("-u", "--up", action="store_true", dest="state_up",
        default=False, help=_("Close events for hosts in the 'UP' state."))
    parser.add_option("-k", "--ok", action="store_true", dest="state_ok",
        default=False, help=_("Close events for services in the 'OK' state."))
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

    # Le script doit être appelé avec au moins une
    # des deux options parmi -k et -u pour être utile.
    if not options.state_up and not options.state_ok:
        parser.error(N_(
            "Either -k or -u must be used. "
            "See %s --help for more information.") % sys.argv[0])
        sys.exit(2)

    try:
        res = close_green(logger, options)
        transaction.commit()
    except Exception: # pylint: disable-msg=W0703
        # W0703: Catch "Exception"
        logger.exception(_('Some error occurred:'))
        transaction.abort()
        sys.exit(1)

    logger.info(
        _("Successfully closed %d events matching the given criteria."),
        res
    )
    sys.exit(0)
