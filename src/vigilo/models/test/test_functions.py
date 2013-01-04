# -*- coding: utf-8 -*-
# Copyright (C) 2006-2013 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for functions module"""
from vigilo.models.functions import sql_escape_like
import unittest

class TestFunctions(unittest.TestCase):
    """Classe de test du module functions."""
   
    def test_sql_escape_like(self):
        """
        Teste les valeurs de retour de la fonction sql_escape_like.
        
        On s'attend à ce que les '*' soient remplacées par '%',
        et à ce que les '?' soient substitués par des '_'.
        Il faut en outre que les '%' et les '_' de la 
        chaîne d'origine soient "échappés" par des '\\'.
        """
        # On vérifie que les '%' sont bien "échappés".
        self.assertEqual(sql_escape_like('%'), '\\%')
        self.assertEqual(sql_escape_like('%aa%aa%'), '\\%aa\\%aa\\%')
        
        # On vérifie que les '_' sont bien "échappés".
        self.assertEqual(sql_escape_like('_'), '\\_')
        self.assertEqual(sql_escape_like('_aa_aa_'), '\\_aa\\_aa\\_')
        
        # On vérifie que les '*' sont bien remplacés par des '%'.
        self.assertEqual(sql_escape_like('*'), '%')
        self.assertEqual(sql_escape_like('*aa*aa*'), '%aa%aa%')
        
        # On vérifie que les '?' sont bien remplacés par des '_'.
        self.assertEqual(sql_escape_like('?'), '_')
        self.assertEqual(sql_escape_like('?aa?aa?'), '_aa_aa_')
        