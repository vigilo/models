# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Ajoute un champ dans la table Host qui référence
le fichier de configuration dans lequel l'hôte
a été défini.
Pour le moment, le champ est optionnel, afin de
permettre aux administrateurs de migrer leur parc.
"""

# pylint: disable-msg=W0613
# W0613: Unused arguments

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

    owner = DBSession.execute(
        'SELECT tableowner '
        'FROM pg_catalog.pg_tables '
        'WHERE schemaname = :schema '
        'AND tablename = :table;',
        params={
            'schema': "public",
            'table': tables.SupItem.__tablename__,
        }).fetchone().tableowner

    MigrationDDL(
        [
            "ALTER TABLE %(fullname)s ADD COLUMN idconffile INTEGER",
            "ALTER TABLE %(fullname)s ADD CONSTRAINT %(fullname)s_idconffile_fkey "
                "FOREIGN KEY(idconffile) REFERENCES %(db_basename)sconffile(idconffile) "
                "ON UPDATE CASCADE ON DELETE CASCADE",

            # Correction des droits sur ConfFile.
            "ALTER TABLE %(db_basename)sconffile OWNER TO %(owner)s",
        ],
        # Le nom de la contrainte dépend du préfixe utilisé.
        context={
            'db_basename': DB_BASENAME,
            'owner': owner,
        }
    ).execute(DBSession, tables.Host.__table__)

    # Nécessite la mise à jour de VigiReport.
    actions.upgrade_vigireport = True
