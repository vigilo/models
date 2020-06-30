# -*- coding: utf-8 -*-
# Copyright (C) 2011-2020 CS GROUP - France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Recrée toutes les clés étrangères (FOREIGN KEY) utilisées dans Vigilo
avec l'option DEFERRABLE INITIALLY IMMEDIATE.

Ce changement permet de mettre en attente la vérification des contraintes
référentielles jusqu'à la fin de la transaction courante, ce qui facilite
certaines opérations au sein de VigiConf.

Voir ticket #791.
"""

# pylint: disable-msg=W0613
# W0613: Unused arguments
# pylint: disable-msg=C0103
# Invalid name "..." (should match ...)

from vigilo.models.session import DBSession, MigrationDDL
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

    fkeys = {
        'confitem.idsupitem': 'supitem.idsupitem',
        'correvent.idcause': 'event.idevent',
        'datapermission.idgroup': 'group.idgroup',
        'datapermission.idusergroup': 'usergroup.idgroup',
        'dependency.idgroup': 'dependencygroup.idgroup',
        'dependency.idsupitem': 'supitem.idsupitem',
        'dependencygroup.iddependent': 'supitem.idsupitem',
        'downtime.author': 'user.user_name',
        'downtime.idstatus': 'downtime_status.idstatus',
        'downtime.idsupitem': 'supitem.idsupitem',
        'event.current_state': 'statename.idstatename',
        'event.idsupitem': 'supitem.idsupitem',
        'event.initial_state': 'statename.idstatename',
        'event.peak_state': 'statename.idstatename',
        'eventhistory.idevent': 'event.idevent',
        'eventsaggregate.idcorrevent': 'correvent.idcorrevent',
        'eventsaggregate.idevent': 'event.idevent',
        'graphgroup.idgraph': 'graph.idgraph',
        'graphgroup.idgroup': 'group.idgroup',
        'graphperfdatasource.idgraph': 'graph.idgraph',
        'graphperfdatasource.idperfdatasource':
            'perfdatasource.idperfdatasource',
        'grouphierarchy.idchild': 'group.idgroup',
        'grouphierarchy.idparent': 'group.idgroup',
        'highlevelservice.idservice': 'supitem.idsupitem',
        'hlshistory.idhls': 'highlevelservice.idservice',
        'hlshistory.idstatename': 'statename.idstatename',
        'host2hostclass.hostname': 'host.name',
        'host2hostclass.idclass': 'hostclass.idclass',
        'host.idconffile': 'conffile.idconffile',
        'host.idhost': 'supitem.idsupitem',
        'impactedhls.idhls': 'highlevelservice.idservice',
        'impactedhls.idpath': 'impactedpath.idpath',
        'impactedpath.idsupitem': 'supitem.idsupitem',
        'lowlevelservice.idcollector': {
            'remote': 'supitem.idsupitem',
            'update': 'ON UPDATE CASCADE',
            'delete': 'ON DELETE SET NULL',
        },
        'lowlevelservice.idhost': 'host.idhost',
        'lowlevelservice.idservice': 'supitem.idsupitem',
        'mapgroup.idgroup': 'group.idgroup',
        'mapgroup.idmap': 'map.idmap',
        'maplink.idfrom_node': 'mapnode.idmapnode',
        'maplink.idmap': 'map.idmap',
        'maplink.idto_node': 'mapnode.idmapnode',
        'mapnode.idmap': 'map.idmap',
        'mapnodehost.idhost': 'host.idhost',
        'mapnodehost.idmapnode': 'mapnode.idmapnode',
        'mapnodeservice.idmapnode': 'mapnode.idmapnode',
        'mapnodeservice.idservice': 'supitem.idsupitem',
        'mapsegment.idmapsegment': 'maplink.idmaplink',
        'mapservicelink.idds_out': 'perfdatasource.idperfdatasource',
        'mapservicelink.idds_in': 'perfdatasource.idperfdatasource',
        'mapservicelink.idgraph': 'graph.idgraph',
        'mapservicelink.idmapservicelink': 'maplink.idmaplink',
        'mapservicelink.idref': 'supitem.idsupitem',
        'perfdatasource.idhost': 'host.idhost',
        'state.idsupitem': 'supitem.idsupitem',
        'state.state': 'statename.idstatename',
        'submapmapnodetable.idmap': 'map.idmap',
        'submapmapnodetable.mapnodeid': 'mapnode.idmapnode',
        'supitemgroup.idgroup': 'group.idgroup',
        'supitemgroup.idsupitem': 'supitem.idsupitem',
        'tag.idsupitem': 'supitem.idsupitem',
        'usergrouppermissions.idgroup': 'usergroup.idgroup',
        'usergrouppermissions.idpermission': 'permission.idpermission',
        'usertousergroups.idgroup': 'usergroup.idgroup',
        'usertousergroups.username': 'user.user_name',
        'ventilation.idapp': 'application.idapp',
        'ventilation.idhost': 'host.idhost',
        'ventilation.idvigiloserver': 'vigiloserver.idvigiloserver',
    }

    drop_stmt = []
    add_stmt = []
    for fkey_name, fkey_data in fkeys.iteritems():
        if not isinstance(fkey_data, dict):
            fkey_data = {'remote': fkey_data}

        table, column = fkey_name.split('.', 2)
        drop_stmt.append(
            'ALTER TABLE vigilo_%(table)s '
            'DROP CONSTRAINT "vigilo_%(fkey)s";' % {
                'table': table,
                'fkey': fkey_name.replace('.', '_') + '_fkey',
            }
        )

        remote_table, remote_column = fkey_data['remote'].split('.', 2)
        add_stmt.append(
            'ALTER TABLE vigilo_%(table)s '
            'ADD CONSTRAINT "vigilo_%(fkey)s" '
            'FOREIGN KEY (%(column)s) '
            'REFERENCES vigilo_%(remote_table)s(%(remote_column)s) '
            '%(on_update)s %(on_delete)s DEFERRABLE INITIALLY IMMEDIATE;' % {
                'table': table,
                'fkey': fkey_name.replace('.', '_') + '_fkey',
                'column': column,
                'remote_table': remote_table,
                'remote_column': remote_column,
                'on_update': fkey_data.get('update', 'ON UPDATE CASCADE'),
                'on_delete': fkey_data.get('delete', 'ON DELETE CASCADE'),
            }
        )

    MigrationDDL(
        drop_stmt + add_stmt,
    ).execute(DBSession, tables.HighLevelService.__table__)
