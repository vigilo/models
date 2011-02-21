# -*- coding: utf-8 -*-
"""
Implémentation de l'arborescence des groupes (de cartes,
de graphes, d'éléments supervisés) sous la forme d'ensembles
imbriqués.

Utilisation d'une racine (groupe "Root") dans chaque type
de groupe (ie. il n'y a plus de poly-arbres / forêts).
"""

from vigilo.models.session import DBSession, ClusteredDDL
from vigilo.models.configure import DB_BASENAME
from vigilo.models import tables

def upgrade(migrate_engine, cluster_name):
    # Ajout des nouvelles colonnes.
    ClusteredDDL(
        [
            "ALTER TABLE %(fullname)s ADD COLUMN tree_left INTEGER",
            "ALTER TABLE %(fullname)s ADD COLUMN tree_right INTEGER",
            "ALTER TABLE %(fullname)s ADD COLUMN depth INTEGER",
        ],
        cluster_name=cluster_name,
        cluster_sets=[2, 3],
        context={
            'db_basename': DB_BASENAME,
        }
    ).execute(DBSession, tables.group.Group.__table__)

    # Récupération du groupe racine pour les cartes.
    map_root = DBSession.execute(
        "SELECT idgroup "
        "FROM %(db_basename)sgroup "
        "WHERE grouptype = 'mapgroup' "
        "AND name = 'Root' "
        "AND NOT EXISTS("
            "SELECT 1 FROM %(db_basename)sgrouphierarchy "
            "WHERE idchild = idgroup "
            "AND hops > 0"
        ")" % {
            'db_basename': DB_BASENAME,
        }).fetchone()

    # Création des "Root" pour les autres types de groupes.
    sig_root = tables.SupItemGroup(name=u'Root')
    DBSession.add(sig_root)
    graph_root = tables.GraphGroup(name=u'Root')
    DBSession.add(graph_root)
    DBSession.flush()

    # Récupération de l'arborescence actuelle.
    children = {}
    for data in DBSession.execute(
        'SELECT idchild, idparent '
        'FROM %(db_basename)sgrouphierarchy '
        'WHERE hops = 1' % {
            'db_basename': DB_BASENAME,
        }):
        children.setdefault(data.idparent, [])
        children[data.idparent].append(data.idchild)

    # Ajout des racines actuels des SupItemGroup/GraphGroup
    # en tant que fils des nouvelles racines.
    children[sig_root.idgroup] = []
    children[graph_root.idgroup] = []
    for data in DBSession.execute(
        "SELECT idgroup, grouptype "
        "FROM %(db_basename)sgroup "
        "WHERE grouptype IN ('supitemgroup', 'graphgroup') "
        "AND NOT EXISTS ("
            "SELECT 1 FROM %(db_basename)sgrouphierarchy "
            "WHERE idchild = idgroup "
            "AND hops > 0"
        ")" % {
            'db_basename': DB_BASENAME,
        }):
        if data.grouptype == u'supitemgroup':
            if data.idgroup != sig_root.idgroup:
                children[sig_root.idgroup].append(data.idgroup)
        elif data.idgroup != graph_root.idgroup:
            children[graph_root.idgroup].append(data.idgroup)

    def update_hierarchy(hierarchy, current_node, index, depth):
        left = index
        right = left + 1
        for child in children.get(current_node, []):
            right = update_hierarchy(hierarchy, child, right, depth + 1) + 1
        DBSession.execute(
            "UPDATE %(db_basename)sgroup "
            "SET tree_left = :left, tree_right = :right, depth = :depth "
            "WHERE idgroup = :idgroup" % {
                'db_basename': DB_BASENAME,
            },
            params={
                'idgroup': current_node,
                'left': left,
                'right': right,
                'depth': depth,
            }
        )
        return right

    print ""
    print "Converting groups of maps to the new system... Please wait."
    print "This may take up a few minutes. "
    print "Please wait until the conversion is completed."
    update_hierarchy(children, map_root.idgroup, 1, 0)

    print ""
    print "Converting groups of graphs to the new system..."
    print "This may take up a few minutes. "
    print "Please wait until the conversion is completed."
    update_hierarchy(children, sig_root.idgroup, 1, 0)

    print ""
    print "Converting groups of monitored items to the new system..."
    print "This may take up a few minutes. "
    print "Please wait until the conversion is completed."
    update_hierarchy(children, graph_root.idgroup, 1, 0)

    # Ajout des contraintes et suppression de la table
    # GroupHierarchy devenue obsolète.
    ClusteredDDL(
        [
            "ALTER TABLE %(fullname)s ALTER COLUMN tree_left SET NOT NULL",
            "ALTER TABLE %(fullname)s ALTER COLUMN tree_right SET NOT NULL",
            "ALTER TABLE %(fullname)s ALTER COLUMN depth SET NOT NULL",
            "DROP TABLE %(db_basename)sgrouphierarchy CASCADE",
        ],
        cluster_name=cluster_name,
        cluster_sets=[2, 3],
        # Nécessaire pour supprimer grouphierarchy.
        context={
            'db_basename': DB_BASENAME,
        }
    ).execute(DBSession, tables.group.Group.__table__)
