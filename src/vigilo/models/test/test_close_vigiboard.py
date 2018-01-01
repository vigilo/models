# -*- coding: utf-8 -*-
# Copyright (C) 2011-2018 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test de fermetures automatique d'événements dans VigiBoard."""
import unittest
import time
from datetime import datetime
import transaction

from vigilo.models.test.controller import setup_db, teardown_db, Options

from vigilo.models.demo import functions as fn
from vigilo.models.scripts.close_vigiboard import close_green
from vigilo.models import tables
from vigilo.models.session import DBSession

from vigilo.common.logging import get_logger
LOGGER = get_logger(__name__)

class TestCloseVigiBoard(unittest.TestCase):
    """
    Teste le script de fermeture automatique des événements
    dans VigiBoard.
    """

    def setUp(self):
        setup_db()
        two_days_ago = datetime.fromtimestamp(time.time() - 2 * 86400)

        localhost = fn.add_host('localhost')
        uptime = fn.add_lowlevelservice(localhost, 'UpTime')
        ping = fn.add_lowlevelservice(localhost, 'Ping')
        users = fn.add_lowlevelservice(localhost, 'Users')

        localhost2 = fn.add_host('localhost2')
        uptime2 = fn.add_lowlevelservice(localhost2, 'UpTime2')

        localhost3 = fn.add_host('localhost3')
        localhost4 = fn.add_host('localhost4')

        # localhost UP : l'événement pourra être fermé (option -u).
        fn.add_correvent([fn.add_event(localhost, 'UP', 'foo')])

        # UpTime OK : l'événement pourra être fermé (option -k).
        fn.add_correvent([fn.add_event(uptime, 'OK', 'foo')])

        # Ping et Users sont en erreur et ne pourront
        # donc pas être fermés automatiquement.
        fn.add_correvent([fn.add_event(ping, 'CRITICAL', 'foo')])
        fn.add_correvent(
            [fn.add_event(users, 'CRITICAL', 'foo', timestamp=two_days_ago)]
        )

        # localhost2 UP et événement ouvert depuis 2j.
        fn.add_correvent(
            [fn.add_event(localhost2, 'UP', 'foo', timestamp=two_days_ago)]
        )

        # UpTime2 OK et événement ouvert depuis 2j.
        fn.add_correvent(
            [fn.add_event(uptime2, 'OK', 'foo', timestamp=two_days_ago)]
        )

        # localhost3 et localhost4 sont en erreur
        # et ne pourront donc pas être fermés.
        fn.add_correvent([fn.add_event(localhost3, 'DOWN', 'foo')])
        fn.add_correvent(
            [fn.add_event(localhost4, 'DOWN', 'foo', timestamp=two_days_ago)]
        )


    def tearDown(self):
        teardown_db()
        DBSession.expunge_all()
        transaction.abort()

    def test_close_unlimited_ok(self):
        """Fermeture événements état OK sans limite de durée."""
        # On veut fermer les événements corrélés qui sont dans l'état OK,
        # quelque soit la date à laquelle ils ont été créés.
        options = Options(state_ok=True, state_up=False, days=None)
        res = close_green(LOGGER, options)
        self.assertTrue(res) # pas d'erreur.

        # On s'assure que les CorrEvent associés à l'état OK
        # ont bien été clos.
        identifiers = [
            (u'localhost', u'UpTime'),
            (u'localhost2', u'UpTime2'),
        ]
        supitems = [
            tables.LowLevelService.by_host_service_name(*identifier)
            for identifier in identifiers
        ]
        events = [
            DBSession.query(tables.Event).filter(
                tables.Event.idsupitem == supitem.idsupitem).one()
            for supitem in supitems
        ]
        correvents = [
            DBSession.query(tables.CorrEvent).filter(
                tables.CorrEvent.idcause == event.idevent).one()
            for event in events
        ]
        for correvent in correvents:
            self.assertEqual(correvent.ack, tables.CorrEvent.ACK_CLOSED)

        # Les autres doivent toujours être dans l'état "nouveau".
        others = DBSession.query(tables.CorrEvent).filter(
                ~tables.CorrEvent.idcorrevent.in_([
                    correvent.idcorrevent for correvent in correvents
                ])
            ).all()
        self.assertNotEquals(0, len(others))
        for other in others:
            self.assertEqual(other.ack, tables.CorrEvent.ACK_NONE,
                "L'événement corrélé sur %s devrait être 'nouveau'" %
                other.cause.supitem
            )


    def test_close_limited_ok(self):
        """Fermeture événements état OK avec limite de durée."""
        # On veut fermer les événements corrélés qui sont dans l'état OK,
        # ayant plus de 1j d'âge.
        options = Options(state_ok=True, state_up=False, days=1)
        res = close_green(LOGGER, options)
        self.assertTrue(res) # pas d'erreur.

        # On s'assure que le CorrEvent associé à l'état OK
        # âgé de 2j a bien été clos.
        supitem = tables.LowLevelService.by_host_service_name(
                    u'localhost2', u'UpTime2')
        event = DBSession.query(tables.Event).filter(
            tables.Event.idsupitem == supitem.idsupitem).one()
        correvent = DBSession.query(tables.CorrEvent).filter(
            tables.CorrEvent.idcause == event.idevent).one()
        self.assertEqual(correvent.ack, tables.CorrEvent.ACK_CLOSED)

        # Les autres doivent toujours être dans l'état "nouveau".
        others = DBSession.query(tables.CorrEvent).filter(
            tables.CorrEvent.idcorrevent != correvent.idcorrevent).all()
        self.assertNotEquals(0, len(others))
        for other in others:
            self.assertEqual(other.ack, tables.CorrEvent.ACK_NONE,
                "L'événement corrélé sur %s devrait être 'nouveau'" %
                other.cause.supitem
            )


    def test_close_unlimited_up(self):
        """Fermeture événements état UP sans limite de durée."""
        # On veut fermer les événements corrélés qui sont dans l'état UP,
        # quelque soit la date à laquelle ils ont été créés.
        options = Options(state_up=True, state_ok=False, days=None)
        res = close_green(LOGGER, options)
        self.assertTrue(res) # pas d'erreur.

        # On s'assure que les CorrEvent associés à l'état UP
        # ont bien été clos.
        identifiers = [
            u'localhost',
            u'localhost2',
        ]
        supitems = [
            tables.Host.by_host_name(identifier)
            for identifier in identifiers
        ]
        events = [
            DBSession.query(tables.Event).filter(
                tables.Event.idsupitem == supitem.idsupitem).one()
            for supitem in supitems
        ]
        correvents = [
            DBSession.query(tables.CorrEvent).filter(
                tables.CorrEvent.idcause == event.idevent).one()
            for event in events
        ]
        for correvent in correvents:
            self.assertEqual(correvent.ack, tables.CorrEvent.ACK_CLOSED)

        # Les autres doivent toujours être dans l'état "nouveau".
        others = DBSession.query(tables.CorrEvent).filter(
                ~tables.CorrEvent.idcorrevent.in_([
                    correvent.idcorrevent for correvent in correvents
                ])
            ).all()
        self.assertNotEquals(0, len(others))
        for other in others:
            self.assertEqual(other.ack, tables.CorrEvent.ACK_NONE,
                "L'événement corrélé sur %s devrait être 'nouveau'" %
                other.cause.supitem
            )

    def test_close_limited_up(self):
        """Fermeture événements état UP avec limite de durée."""
        # On veut fermer les événements corrélés qui sont dans l'état UP,
        # ayant au moins 1j d'âge.
        options = Options(state_up=True, state_ok=False, days=1)
        res = close_green(LOGGER, options)
        self.assertTrue(res) # pas d'erreur.

        # On s'assure que le CorrEvent associé à l'état UP
        # âgé de 2j a bien été clos.
        supitem = tables.Host.by_host_name(u'localhost2')
        event = DBSession.query(tables.Event).filter(
            tables.Event.idsupitem == supitem.idsupitem).one()
        correvent = DBSession.query(tables.CorrEvent).filter(
            tables.CorrEvent.idcause == event.idevent).one()
        self.assertEqual(correvent.ack, tables.CorrEvent.ACK_CLOSED)

        # Les autres doivent toujours être dans l'état "nouveau".
        others = DBSession.query(tables.CorrEvent).filter(
            tables.CorrEvent.idcorrevent != correvent.idcorrevent).all()
        self.assertNotEquals(0, len(others))
        for other in others:
            self.assertEqual(other.ack, tables.CorrEvent.ACK_NONE,
                "L'événement corrélé sur %s devrait être 'nouveau'" %
                other.cause.supitem
            )
