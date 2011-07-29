# -*- coding: utf-8 -*-
"""
Renomme les clés étrangères dans la table MapServiceLink.

Les clés étrangères "mapservicelink_idds_from_to_to_fkey" et
"mapservicelink_idds_to_to_from_fkey" de MapServiceLink s'appellent
désormais (respectivement) "mapservicelink_idds_out_fkey" et
"mapservicelink_idds_in_fkey".

Ce changement était déjà pris en compte dans les installations
réalisées APRÈS l'application de la migration 011. Il n'avait
pas été réalisé pour les installations antérieures.

À l'issue de ce changement, une meilleure cohérence/stabilité
est obtenue pour les différentes installations.
"""

from vigilo.models.session import DBSession, MigrationDDL
from vigilo.models.configure import DB_BASENAME
from vigilo.models import tables

def upgrade(migrate_engine, actions):
    """
    Migre le modèle.

    @param migrate_engine: Connexion à la base de données,
        pouvant être utilisée durant la migration.
    @type migrate_engine: C{Engine}
    @param actions: Conteneur listant les actions à effectuer
        lorsque cette migration aura été appliquée.
    @type actions: C{MigrationActions}
    """

    found = DBSession.execute(
        "SELECT COUNT(*) AS found "
        "FROM pg_catalog.pg_constraint "
        "WHERE conname = :constraint",
        params={
            'constraint': '%smapservicelink_idds_in_fkey' % DB_BASENAME,
        }).fetchone().found

    # Si le modèle a été installé après la migration 011,
    # les clés étrangères ont déjà le bon nom et il n'y a
    # rien à faire.
    if found:
        return

    MigrationDDL(
        [
            # Suppression des anciennes clés étrangères.
            # 1. idds_from_to_to
            "ALTER TABLE %(db_basename)s%(table)s "
            "DROP CONSTRAINT %(db_basename)s%(table)s_idds_from_to_to_fkey",
            # 2. idds_to_to_from
            "ALTER TABLE %(db_basename)s%(table)s "
            "DROP CONSTRAINT %(db_basename)s%(table)s_idds_to_to_from_fkey",

            # Création des nouvelles clés.
            # 1. idds_out
            'ALTER TABLE %(db_basename)s%(table)s '
            'ADD CONSTRAINT "%(db_basename)s%(table)s_idds_out_fkey" '
            'FOREIGN KEY (idds_out) '
            'REFERENCES %(db_basename)s%(remote_table)s(%(remote_column)s) '
            'ON UPDATE CASCADE ON DELETE CASCADE',
            # 2. idds_in
            'ALTER TABLE %(db_basename)s%(table)s '
            'ADD CONSTRAINT "%(db_basename)s%(table)s_idds_in_fkey" '
            'FOREIGN KEY (idds_in) '
            'REFERENCES %(db_basename)s%(remote_table)s(%(remote_column)s) '
            'ON UPDATE CASCADE ON DELETE CASCADE',
        ],
        context={
            'db_basename': DB_BASENAME,
            'table': 'mapservicelink',
            'remote_table': 'perfdatasource',
            'remote_column': 'idperfdatasource',
        }
    ).execute(DBSession, tables.HighLevelService.__table__)
