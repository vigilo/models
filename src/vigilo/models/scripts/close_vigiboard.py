# -*- coding: utf-8 -*-
"""
Script permettant de refermer automatiquement les événements
se trouvant dans l'état OK et/ou UP dans VigiBoard.
"""

import sys, os
import transaction
from datetime import datetime
from optparse import OptionParser
import pwd # Disponible uniquement sur Unix-like

__all__ = (
    'close_green',
)

def close_green(*args):
    """
    Cette fonction ferme les événements qui apparaissent
    en vert dans VigiBoard (c'est-à-dire ceux dans l'état
    "OK" ou "UP").
    """

    from vigilo.common.gettext import translate
    _ = translate(__name__)

    parser = OptionParser()
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
    LOGGER = get_logger(__name__)

    if args:
        LOGGER.error(_('Too many arguments'))
        sys.exit(1)

    from vigilo.models.configure import configure_db
    try:
        configure_db(settings['database'], 'sqlalchemy_',
            settings['database']['db_basename'])
    except KeyError:
        LOGGER.error(_('No database configuration found'))
        sys.exit(1)

    from vigilo.models.session import DBSession
    from vigilo.models.tables import Event, CorrEvent, StateName, EventHistory

    sought_states = []
    if options.state_up:
        sought_states.append(u'UP')
    if options.state_ok:
        sought_states.append(u'OK')

    # Le script doit être appelé avec au moins une
    # des deux options parmi -k et -u pour être utile.
    if not sought_states:
        parser.print_usage()
        sys.exit(1)

    events = DBSession.query(
            CorrEvent
        ).join(
            (Event, Event.idevent == CorrEvent.idcause),
            (StateName, StateName.idstatename == Event.current_state),
        ).filter(StateName.statename.in_(sought_states)
        ).filter(CorrEvent.status != u'AAClosed').all()

    for event in events:
        # On ajoute un message dans l'historique pour la traçabilité.
        history = EventHistory(
                type_action=u"Acknowledgement change state",
                idevent=event.idcause,
                value=u"",
                text=u"Automatically marked the event as closed",
                username=pwd.getpwuid(os.getuid())[0],
                timestamp=datetime.now(),
            )
        DBSession.add(history)

        # On referme l'événement.
        event.status = u"AAClosed"
        DBSession.flush()

    transaction.commit()
    LOGGER.info(
        _("Successfully closed %d events matching the given criteria."),
        len(events)
    )
    sys.exit(0)
