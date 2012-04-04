# -*- coding: utf-8 -*-
# Copyright (C) 2006-2012 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Teste le fonctionnement général du mécanisme
de migration de la base de données.
"""

import unittest

import transaction

from vigilo.models.session import DBSession
from vigilo.models import tables
from vigilo.models.websetup import get_migration_scripts, \
                                migrate_model, populate_db

from vigilo.models.test.controller import setup_db, teardown_db


class TestMigration(unittest.TestCase):
    """Teste le fonctionnement général des migrations."""

    def setUp(self):
        setup_db()
        # On supprime les noms d'états insérés par défaut.
        # La migration les recréera de toutes façons.
        DBSession.query(tables.StateName).delete()
        DBSession.flush()

    def tearDown(self):
        DBSession.rollback()
        DBSession.expunge_all()
        teardown_db()
        transaction.begin()

    def test_model_creation(self):
        """Teste la création du modèle."""
        # On vérifie que lorsque le modèle de Vigilo est créé,
        # il l'est avec la toute dernière version disponible.
        populate_db(DBSession.bind)
        installed_version = DBSession.query(tables.Version).filter(
            tables.Version.name == u'vigilo.models').one()
        scripts = get_migration_scripts('vigilo.models')
        latest_version = max(scripts.keys())
        self.assertEquals(installed_version.version, latest_version)

    def test_migration(self):
        """Teste la migration (partielle/totale) du modèle."""

        # Recherche des scripts de migration dans le dossier des tests.
        module = u'vigilo.models.test.testdata'
        scripts = get_migration_scripts(module)

        expected_scripts = {
            1: '001_Initial_version',
            2: '002_Dummy',
            3: '003_Dummy',
        }
        self.assertEquals(scripts, expected_scripts)

        # On simule l'installation d'un nouveau modèle.
        DBSession.add(tables.Version(
            name=module,
            version=1,
        ))
        DBSession.flush()

        # On vérifie qu'une migration jusqu'à un point fixe fonctionne.
        migrate_model(DBSession.bind, module, scripts, 2)
        version = DBSession.query(tables.Version).filter(
            tables.Version.name == module).one()
        self.assertEquals(version.version, 2)

        # On annule la migration et on teste cette fois une migration
        # jusqu'à la dernière version disponible.
        version.version = 1
        DBSession.flush()
        migrate_model(DBSession.bind, module, scripts)
        version = DBSession.query(tables.Version).filter(
            tables.Version.name == module).one()
        self.assertEquals(version.version, 3)
