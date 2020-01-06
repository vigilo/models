# -*- coding: utf-8 -*-
# Copyright (C) 2006-2020 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for SupItem.get_supitem"""
import unittest

from vigilo.models.session import DBSession
from vigilo.models.demo import functions
from vigilo.models.tables import SupItem

from vigilo.models.test.controller import setup_db, teardown_db


class TestGetSupItem(unittest.TestCase):
    """Test de la méthode get_supitem de la classe 'SupItem'"""

    def runTest(self):
        """
        Test de la récupération dans la BDD de l'identifiant d'un
        item (hôte, service de haut niveau, ou service de bas niveau).
        """
        setup_db()
        DBSession.flush()

        host1 = functions.add_host(u'messagerie')
        lls1 = functions.add_lowlevelservice(host1, u'Processes')
        hls1 = functions.add_highlevelservice(u'Connexion')

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
