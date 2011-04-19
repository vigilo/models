# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for StateName class"""
import unittest
from nose.tools import assert_equals
from controller import setup_db, teardown_db

from vigilo.models.session import DBSession
from vigilo.models.tables import Host, LowLevelService, HighLevelService, \
                                    SupItem, StateName

class TestGetSupItem(unittest.TestCase):
    """Test de la méthode get_supitem de la classe 'SupItem'"""

    def runTest(self):
        """
        Test de la récupération dans la BDD de l'identifiant d'un
        item (hôte, service de haut niveau, ou service de bas niveau).
        """
        setup_db()
        DBSession.add(StateName(statename=u'OK', order=1))
        DBSession.add(StateName(statename=u'UP', order=1))
        DBSession.flush()
        # Ajout d'un hôte dans la BDD
        host1 = Host(
            name = u'messagerie',
            checkhostcmd = u'check11',
            snmpcommunity = u'com11',
            hosttpl = u'tpl11',
            address = u'192.168.0.11',
            snmpport = 11,
            weight = 42,
        )
        DBSession.add(host1)
        DBSession.flush()

        # Ajout d'un service de bas niveau dans la BDD
        lls1 = LowLevelService(
            servicename = u'Processes',
            host = host1,
            command = u'halt',
            weight = 42,
        )
        DBSession.add(lls1)
        DBSession.flush()

        # Ajout d'un service de haut niveau dans la BDD
        hls1 = HighLevelService(
            servicename = u'Connexion',
            message = u'Ouch',
            warning_threshold = 300,
            critical_threshold = 150,
            priority = 1,
        )
        DBSession.add(hls1)
        DBSession.flush()

        # On vérifie que la fonction get_supitem renvoie bien l'identifiant
        # du host1 lorsqu'on lui passe son nom en paramètre.
        self.assertEqual(host1.idhost, SupItem.get_supitem(host1.name, None))

        # On vérifie que la fonction get_supitem renvoie bien l'identifiant
        # du hls1 lorsqu'on lui passe son nom en paramètre.
        self.assertEqual(hls1.idservice,
                         SupItem.get_supitem(None, hls1.servicename))

        # On vérifie que la fonction get_supitem renvoie bien l'identifiant
        # du lls1 lorsqu'on lui passe son nom en paramètre.
        self.assertEqual(lls1.idservice,
                         SupItem.get_supitem(host1.name, lls1.servicename))

        #Nettoyage de la BDD à la fin du test
        del host1
        del lls1
        del hls1
        DBSession.rollback()
        DBSession.expunge_all()
        teardown_db()
