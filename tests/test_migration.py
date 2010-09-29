# -*- coding: utf-8 -*-
"""
Teste les migrations du modèle.
"""

import unittest
from controller import setup_db, teardown_db
from vigilo.models.session import DBSession, ClusteredDDL
from vigilo.models import tables
from vigilo.models.websetup import get_migration_scripts, \
                                migrate_model, populate_db
import transaction

class TestMigration(unittest.TestCase):
    def setUp(self):
        setup_db()

    def tearDown(self):
        DBSession.rollback()
        DBSession.expunge_all()
        teardown_db()
        transaction.begin()

    def test_model_creation(self):
        # On vérifie que lorsque le modèle de Vigilo est créé,
        # il l'est avec la toute dernière version disponible.
        populate_db(DBSession.bind)
        installed_version = DBSession.query(tables.Version).filter(
            tables.Version.name == u'vigilo.models').one()
        scripts = get_migration_scripts('vigilo.models')
        latest_version = max(scripts.keys())
        self.assertEquals(installed_version.version, latest_version)

    def test_migration(self):
        # Recherche des scripts de migration dans le dossier des tests.
        module = u'testdata'
        scripts = get_migration_scripts(module)

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
