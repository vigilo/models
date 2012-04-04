# -*- coding: utf-8 -*-
# Copyright (C) 2011-2012 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test de fermetures automatique d'événements dans VigiBoard."""

import unittest
import time
from datetime import datetime

import transaction

from vigilo.common.logging import get_logger
LOGGER = get_logger(__name__)

from vigilo.models.demo import functions as fn
from vigilo.models.scripts.purge_vigiboard import clean_vigiboard
from vigilo.models import tables
from vigilo.models.session import DBSession

from vigilo.models.test.controller import setup_db, teardown_db, Options


class TestPurgeVigiBoard(unittest.TestCase):
    """
    Teste le script de purge automatique des événements
    de VigiBoard.
    """

    def setUp(self):
        setup_db()
        two_days_ago = datetime.fromtimestamp(time.time() - 2 * 86400)

        localhost = fn.add_host('localhost')
        localhost2 = fn.add_host('localhost2')
        localhost3 = fn.add_host('localhost3')
        localhost4 = fn.add_host('localhost4')

        hls = fn.add_highlevelservice('hls')

        fn.add_correvent(
            [fn.add_event(localhost, 'UP', 'foo')],
            status=tables.CorrEvent.ACK_CLOSED,
        )

        fn.add_correvent(
            [fn.add_event(localhost2, 'UP', 'foo')],
            status=tables.CorrEvent.ACK_CLOSED,
            timestamp=two_days_ago,
        )

        fn.add_correvent(
            [fn.add_event(localhost3, 'UP', 'foo')],
            status=tables.CorrEvent.ACK_NONE,
        )

        fn.add_correvent(
            [fn.add_event(localhost4, 'UP', 'foo')],
            status=tables.CorrEvent.ACK_NONE,
            timestamp=two_days_ago,
        )

        DBSession.add(tables.HLSHistory(
            hls=hls,
            idstatename=tables.StateName.statename_to_value(u'OK'),
            timestamp=two_days_ago,
        ))

        DBSession.add(tables.HLSHistory(
            hls=hls,
            idstatename=tables.StateName.statename_to_value(u'OK'),
            timestamp=datetime.now(),
        ))


    def tearDown(self):
        DBSession.expunge_all()
        transaction.abort()
        teardown_db()


    def test_purge_one_day(self):
        """Purge des événements de plus de 1 jour."""
        # On veut fermer les événements corrélés qui sont dans l'état OK,
        # quelque soit la date à laquelle ils ont été créés.
        options = Options(days=1, size=None)
        clean_vigiboard(LOGGER, options, None)

        # L'entrée d'historique pour un HLS âgée
        # de 2j doit avoir été supprimée.
        self.assertEquals(1, DBSession.query(tables.HLSHistory).count())

        # On s'assure que le CorrEvent et l'événement sur localhost2
        # âgés de 2j ont bien été supprimés.
        supitem = tables.Host.by_host_name(u'localhost2')
        event = DBSession.query(tables.Event).filter(
            tables.Event.idsupitem == supitem.idsupitem).first()
        self.assertEquals(None, event) # sans Event, pas de CorrEvent possible.

        # Les autres doivent être dans l'état "nouveau",
        # sauf l'événement sur localhost qui doit toujours être "fermé".
        others = DBSession.query(tables.CorrEvent).all()
        self.assertNotEquals(0, len(others))

        supitem = tables.Host.by_host_name(u'localhost')
        for other in others:
            # Contourne le problème du support incomplet des contraintes
            # référentielles de type ON DELETE CASCADE dans SQLite.
            if other.cause is None:
                continue

            if other.cause.idsupitem == supitem.idsupitem:
                self.assertEquals(
                    other.ack,
                    tables.CorrEvent.ACK_CLOSED,
                    "L'événement corrélé sur %s devrait être 'fermé'" %
                        other.cause.supitem
                )
            else:
                self.assertEquals(
                    other.ack,
                    tables.CorrEvent.ACK_NONE,
                    "L'événement corrélé sur %s devrait être 'nouveau'" %
                        other.cause.supitem
                )


    def test_purge_zero_days(self):
        """Purge des événements sans limite d'âge."""
        # On veut fermer les événements corrélés qui sont dans l'état OK,
        # quelque soit la date à laquelle ils ont été créés.
        options = Options(days=0, size=None)
        clean_vigiboard(LOGGER, options, None)

        # Les 2 entrées d'historique pour un HLS
        # doivent avoir été supprimées.
        self.assertEquals(0, DBSession.query(tables.HLSHistory).count())

        # On s'assure que le CorrEvent et l'événement sur localhost2
        # âgés de 2j ont bien été supprimés.
        supitem = tables.Host.by_host_name(u'localhost2')
        event = DBSession.query(tables.Event).filter(
            tables.Event.idsupitem == supitem.idsupitem).first()
        self.assertEquals(None, event) # sans Event, pas de CorrEvent possible.

        # Les autres doivent toujours être dans l'état "fermé".
        others = DBSession.query(tables.CorrEvent).all()

        self.assertNotEquals(0, len(others))
        for other in others:
            # Contourne le problème du support incomplet des contraintes
            # référentielles de type ON DELETE CASCADE dans SQLite.
            if other.cause is None:
                continue

            self.assertEquals(
                other.ack,
                tables.CorrEvent.ACK_NONE,
                "L'événement corrélé sur %s devrait être 'nouveau'" %
                    other.cause.supitem
            )
