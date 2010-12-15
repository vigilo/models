# -*- coding: utf-8 -*-
"""
Ajoute un champ dans la table Host qui référence
le fichier de configuration dans lequel l'hôte
a été défini.
Pour le moment, le champ est optionnel, afin de
permettre aux administrateurs de migrer leur parc.
"""

from vigilo.models.session import DBSession, ClusteredDDL
from vigilo.models.configure import DB_BASENAME
from vigilo.models import tables

def upgrade(migrate_engine, cluster_name):
    ClusteredDDL(
        [
            "ALTER TABLE %(fullname)s ADD COLUMN idconffile INTEGER",
            "ALTER TABLE %(fullname)s ADD CONSTRAINT %(fullname)s_idconffile_fkey "
                "FOREIGN KEY(idconffile) REFERENCES %(db_basename)sconffile(idconffile) "
                "ON UPDATE CASCADE ON DELETE CASCADE",
        ],
        cluster_name=cluster_name,
        cluster_sets=[2, 3],
        # Le nom de la contrainte dépend du préfixe utilisé.
        context={
            'db_basename': DB_BASENAME,
        }
    ).execute(DBSession, tables.Host.__table__)
