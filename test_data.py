# -*- coding: utf-8 -*-
"""Insère des données de test dans la base de données."""

import atexit
from vigilo.common.conf import settings
settings.load_module('vigilo.models')

from vigilo.models.configure import configure_db
configure_db(settings['database'], 'sqlalchemy_',
	settings['database']['db_basename'])

from vigilo.models.session import DBSession
from vigilo.models import tables
from vigilo.models.tables.grouphierarchy import GroupHierarchy

def commit_on_exit():
    """
    Effectue un COMMIT sur la transaction à la fin de l'exécution
    du script d'insertion des données de test.
    """
    import transaction
    transaction.commit()

atexit.register(commit_on_exit)

## Etats possibles de la mise en silence pour maintenance
#DBSession.add(tables.DowntimeStatus(status=u'Planified',))
#DBSession.add(tables.DowntimeStatus(status=u'Enabled',))
#DBSession.add(tables.DowntimeStatus(status=u'Finished',))
#DBSession.add(tables.DowntimeStatus(status=u'Cancelled',))
#DBSession.flush()

# Affectation des permissions aux groupes d'utilisateurs.
managers = tables.UserGroup.by_group_name(u'managers')

# Host
def add_Host(name):
    name = u'' + name

    DBSession.add(tables.Host(
        name=name,
        checkhostcmd=u'checkcmd',
        snmpcommunity=u'public',
        snmpport=42,
        snmpoidsperpdu=42,
        snmpversion=u'3',
        hosttpl=u'tpl',
        mainip=u'127.0.0.1',
        weight=42,
    ))
    DBSession.flush()

add_Host('ajc.fw.1')
add_Host('ajc.linux1')
add_Host('ajc.sw.1')
add_Host('bdx.fw.1')
add_Host('bdx.linux1')
add_Host('brouteur')
add_Host('bst.fw.1')
add_Host('bst.unix0')
add_Host('bst.unix1')
add_Host('bst.win0')
add_Host('messagerie')
add_Host('par.fw.1')
add_Host('par.linux0')
add_Host('par.linux1')
add_Host('par.unix0')
add_Host('proto4')
add_Host('server.mails')
add_Host('testaix')
add_Host('testnortel')
add_Host('testsolaris')
add_Host('host1.example.com')
add_Host('host2.example.com')
add_Host('host3.example.com')
add_Host('routeur1')
add_Host('routeur2')
add_Host('firewall')
add_Host('localhost')

# LowLevelService
def add_LowLevelService(name, hostident, weight=100):
    name = u'' + name
    kwargs = {
        'servicename': name,
        'op_dep': u'&',
        'command': u'halt',
        'weight': weight,
    }

    if isinstance(hostident, int):
        kwargs['idhost'] = hostident
    elif isinstance(hostident, basestring):
        host = tables.Host.by_host_name(u'' + hostident)
        kwargs['host'] = host
    else:
        kwargs['host'] = hostident

    DBSession.add(tables.LowLevelService(**kwargs))
    DBSession.flush()

add_LowLevelService('Interface eth0', 'host1.example.com')
add_LowLevelService('Interface eth0', 'host2.example.com')
add_LowLevelService('Interface eth0', 'messagerie')
add_LowLevelService('Interface eth0', 'routeur1')
add_LowLevelService('Interface eth0', 'routeur2')
add_LowLevelService('Interface eth0', 'firewall')
add_LowLevelService('Interface eth1', 'host2.example.com', weight=120)
add_LowLevelService('Interface eth1', 'host3.example.com')
add_LowLevelService('Interface eth1', 'routeur1')
add_LowLevelService('Interface eth1', 'routeur2')
add_LowLevelService('Interface eth1', 'firewall')
add_LowLevelService('Interface eth2', 'host2.example.com', weight=130)
add_LowLevelService('UpTime', 'brouteur')
add_LowLevelService('UpTime', 'messagerie')
add_LowLevelService('UpTime', 'proto4')
add_LowLevelService('UpTime', 'host1.example.com')
add_LowLevelService('UpTime', 'host2.example.com')
add_LowLevelService('CPU', 'brouteur')
add_LowLevelService('CPU', 'messagerie')
add_LowLevelService('CPU', 'proto4')
add_LowLevelService('CPU', 'host1.example.com')
add_LowLevelService('CPU', 'host2.example.com')
add_LowLevelService('Load', 'brouteur')
add_LowLevelService('Load', 'proto4')
add_LowLevelService('Load', 'messagerie')
add_LowLevelService('Load', 'host1.example.com')
add_LowLevelService('Load', 'host2.example.com')
add_LowLevelService('Processes', 'brouteur')
add_LowLevelService('Processes', 'messagerie')
add_LowLevelService('Processes', 'proto4')
add_LowLevelService('Processes', 'host1.example.com')
add_LowLevelService('Processes', 'host2.example.com')
add_LowLevelService('HTTPD', 'host1.example.com')
add_LowLevelService('HTTPD', 'host2.example.com')
add_LowLevelService('RAM', 'messagerie')
add_LowLevelService('RAM', 'proto4')
add_LowLevelService('RAM', 'brouteur')
add_LowLevelService('RAM', 'host1.example.com')
add_LowLevelService('RAM', 'host2.example.com')
add_LowLevelService('perfdatasource', 'localhost')
add_LowLevelService('SSH', 'localhost')
add_LowLevelService('HTTP', 'localhost')
add_LowLevelService('Root Partition', 'localhost')
add_LowLevelService('Swap Usage', 'localhost')


# HighLevelService
DBSession.add(tables.HighLevelService(
    servicename=u'Connexion',
    op_dep=u'+',
    message=u'Ouch',
    warning_threshold=300,
    critical_threshold=150,
    weight=None,
    priority=3,
))
DBSession.flush()

DBSession.add(tables.HighLevelService(
    servicename=u'Portail web',
    op_dep=u'&',
    message=u'Ouch',
    warning_threshold=300,
    critical_threshold=150,
    weight=None,
    priority=1,
))
DBSession.flush()

# Dependency
def add_Dependency(dependent, depended):
    kwargs = {}

    if isinstance(dependent, int):
        kwargs['idsupitem1'] = dependent
    else:
        host, service = dependent
        if host is None:        # HLS
            kwargs['supitem1'] = \
                tables.HighLevelService.by_service_name(u'' + service)
        elif service is None:   # Host
            kwargs['supitem1'] = tables.Host.by_host_name(u'' + host)
        else:                   # LLS
            kwargs['supitem1'] = \
                tables.LowLevelService.by_host_service_name(
                    u'' + host, u'' + service)

    if isinstance(depended, int):
        kwargs['idsupitem2'] = depended
    else:
        host, service = depended
        if host is None:        # HLS
            kwargs['supitem2'] = \
                tables.HighLevelService.by_service_name(u'' + service)
        elif service is None:   # Host
            kwargs['supitem2'] = tables.Host.by_host_name(u'' + host)
        else:                   # LLS
            kwargs['supitem2'] = \
                tables.LowLevelService.by_host_service_name(
                    u'' + host, u'' + service)

    DBSession.add(tables.Dependency(**kwargs))
    DBSession.flush()

add_Dependency((None, 'Connexion'), ('host2.example.com', 'Interface eth0'))
add_Dependency((None, 'Connexion'), ('host2.example.com', 'Interface eth1'))
add_Dependency((None, 'Connexion'), ('host2.example.com', 'Interface eth2'))
add_Dependency((None, 'Portail web'), (None, 'Connexion'))
add_Dependency((None, 'Portail web'), ('host2.example.com', 'HTTPD'))
add_Dependency(('messagerie', 'Processes'), ('messagerie', 'CPU'))
add_Dependency(('messagerie', 'Processes'), ('messagerie', 'RAM'))
add_Dependency(('messagerie', 'CPU'), ('messagerie', 'Interface eth0'))
add_Dependency(('messagerie', 'RAM'), ('messagerie', 'Interface eth0'))
add_Dependency(('messagerie', 'Interface eth0'), ('routeur1', 'Interface eth1'))
add_Dependency(('messagerie', 'Interface eth0'), ('routeur2', 'Interface eth1'))
add_Dependency(('host1.example.com', 'Processes'), ('host1.example.com', 'CPU'))
add_Dependency(('host1.example.com', 'Processes'), ('host1.example.com', 'RAM'))
add_Dependency(('host1.example.com', 'CPU'), ('host1.example.com', 'Interface eth0'))
add_Dependency(('host1.example.com', 'RAM'), ('host1.example.com', 'Interface eth0'))
add_Dependency(('host1.example.com', 'Interface eth0'), ('firewall', 'Interface eth1'))
add_Dependency(('firewall', 'Interface eth1'), ('firewall', 'Interface eth0'))
add_Dependency(('firewall', 'Interface eth0'), ('routeur1', 'Interface eth1'))
add_Dependency(('firewall', 'Interface eth0'), ('routeur2', 'Interface eth1'))
add_Dependency(('routeur1', 'Interface eth1'), ('routeur1', 'Interface eth0'))
add_Dependency(('routeur2', 'Interface eth1'), ('routeur2', 'Interface eth0'))

# SupItemGroup
servers = tables.SupItemGroup(name=u'Serveurs')
DBSession.add(servers)
DBSession.flush()

linux = tables.SupItemGroup(name=u'Serveurs Linux')
DBSession.add(linux)
DBSession.flush()

windows = tables.SupItemGroup(name=u'Serveurs Windows')
DBSession.add(windows)
DBSession.flush()

# GraphGroup
graphes = tables.GraphGroup(name=u'Graphes')
DBSession.add(graphes)
DBSession.flush()


# Ajout des boucles.
DBSession.add(GroupHierarchy(parent=servers, child=servers, hops=0))
DBSession.add(GroupHierarchy(parent=linux, child=linux, hops=0))
DBSession.add(GroupHierarchy(parent=windows, child=windows, hops=0))
DBSession.add(GroupHierarchy(parent=graphes, child=graphes, hops=0))

# Ajout de la hiérarchie.
DBSession.add(GroupHierarchy(parent=servers, child=linux, hops=1))
DBSession.add(GroupHierarchy(parent=servers, child=windows, hops=1))
DBSession.flush()

# Affectation des permissions aux groupes d'hôtes.
def add_SupItemGroupPermission(group, perm):
    if isinstance(group, basestring):
        group = tables.SupItemGroup.by_group_name(u'' + group)

    if isinstance(perm, basestring):
        perm = tables.Permission.by_permission_name(u'' + perm)

    group.permissions.append(perm)
    DBSession.flush()

add_SupItemGroupPermission('Serveurs', 'manage')

# Affectation des hôtes aux groupes d'hôtes.
def add_Host2SupItemGroup(host, group):
    if isinstance(group, basestring):
        group = tables.SupItemGroup.by_group_name(u'' + group)

    if isinstance(host, basestring):
        host = tables.Host.by_host_name(u'' + host)

    group.supitems.append(host)
    DBSession.flush()

add_Host2SupItemGroup('ajc.fw.1', 'Serveurs')
add_Host2SupItemGroup('ajc.linux1', 'Serveurs Linux')
add_Host2SupItemGroup('ajc.sw.1', 'Serveurs')
add_Host2SupItemGroup('bdx.fw.1', 'Serveurs')
add_Host2SupItemGroup('bdx.linux1', 'Serveurs Linux')
add_Host2SupItemGroup('brouteur', 'Serveurs')
add_Host2SupItemGroup('bst.fw.1', 'Serveurs')
add_Host2SupItemGroup('bst.unix0', 'Serveurs')
add_Host2SupItemGroup('bst.unix1', 'Serveurs Linux')
add_Host2SupItemGroup('bst.win0', 'Serveurs Windows')
add_Host2SupItemGroup('messagerie', 'Serveurs Linux')
add_Host2SupItemGroup('par.fw.1', 'Serveurs Linux')
add_Host2SupItemGroup('par.linux0', 'Serveurs Linux')
add_Host2SupItemGroup('par.linux1', 'Serveurs Linux')
add_Host2SupItemGroup('par.unix0', 'Serveurs Linux')
add_Host2SupItemGroup('proto4', 'Serveurs Linux')
add_Host2SupItemGroup('server.mails', 'Serveurs Linux')
add_Host2SupItemGroup('testaix', 'Serveurs Windows')
add_Host2SupItemGroup('testnortel', 'Serveurs Windows')
add_Host2SupItemGroup('testsolaris', 'Serveurs Windows')
add_Host2SupItemGroup('host1.example.com', 'Serveurs Linux')
add_Host2SupItemGroup('host2.example.com', 'Serveurs Linux')
add_Host2SupItemGroup('host3.example.com', 'Serveurs Linux')
add_Host2SupItemGroup('routeur1', 'Serveurs Linux')
add_Host2SupItemGroup('routeur2', 'Serveurs Linux')
add_Host2SupItemGroup('firewall', 'Serveurs Linux')
add_Host2SupItemGroup('localhost', 'Serveurs Windows')

# Affectation des hôtes aux groupes d'hôtes.
def add_LowLevelService2SupItemGroup(lls, group):
    if isinstance(group, basestring):
        group = tables.SupItemGroup.by_group_name(u'' + group)

    if isinstance(lls, tuple):
        lls = tables.LowLevelService.by_host_service_name(*lls)

    group.supitems.append(lls)
    DBSession.flush()

add_LowLevelService2SupItemGroup((u'localhost', u'SSH'), 'Serveurs Linux')

# Application
def add_Application(name):
    DBSession.add(tables.Application(name=u'' + name))
    DBSession.flush()

add_Application('nagios')
add_Application('rrdgraph')
add_Application('collector')
add_Application('connector-nagios')

# VigiloServer
def add_VigiloServer(name):
    DBSession.add(tables.VigiloServer(
        name=u'' + name,
    ))
    DBSession.flush()

add_VigiloServer('localhost')

# Ventilation
def add_Ventilation(host, vigiloserver, app):
    kwargs = {}

    if isinstance(host, basestring):
        kwargs['host'] = tables.Host.by_host_name(u'' + host)
    elif isinstance(host, int):
        kwargs['idhost'] = host
    else:
        kwargs['host'] = host

    if isinstance(vigiloserver, basestring):
        kwargs['vigiloserver'] = tables.VigiloServer.by_vigiloserver_name(
                                        u'' + vigiloserver)
    elif isinstance(vigiloserver, int):
        kwargs['idvigiloserver'] = vigiloserver
    else:
        kwargs['vigiloserver'] = vigiloserver

    if isinstance(app, basestring):
        kwargs['application'] = tables.Application.by_app_name(u'' + app)
    elif isinstance(app, int):
        kwargs['idapp'] = app
    else:
        kwargs['application'] = app

    DBSession.add(tables.Ventilation(**kwargs))
    DBSession.flush()

# add_Ventilation(h1, h2, app)
# L'appli app pour h1 se trouve sur h2.
add_Ventilation('localhost', 'localhost', 'rrdgraph')
add_Ventilation('localhost', 'localhost', 'nagios')
add_Ventilation('proto4', 'localhost', 'rrdgraph')

# Installation
def add_Installation(vigiloserver, app, jid):
    kwargs = {}

    if isinstance(vigiloserver, basestring):
        kwargs['vigiloserver'] = tables.VigiloServer.by_vigiloserver_name(
                                        u'' + vigiloserver)
    elif isinstance(vigiloserver, int):
        kwargs['idvigiloserver'] = vigiloserver
    else:
        kwargs['vigiloserver'] = vigiloserver

    if isinstance(app, basestring):
        kwargs['application'] = tables.Application.by_app_name(u'' + app)
    elif isinstance(app, int):
        kwargs['idapp'] = app
    else:
        kwargs['application'] = app

    kwargs['jid'] = u'' + jid

    DBSession.add(tables.Installation(**kwargs))
    DBSession.flush()


# Sources de données de métrologie (PerfDataSource)
def add_PerfDataSource(service, name, type='COUNTER', factor=1):
    kwargs = {
        'name': unicode(name),
        'type': unicode(type),
        'factor': factor,
    }

    if isinstance(service, tuple):
        kwargs['service'] = tables.LowLevelService. \
                                by_host_service_name(*service)
    elif isinstance(service, int):
        kwargs['idservice'] = service
    else:
        kwargs['service'] = service

    pds = tables.PerfDataSource(**kwargs)
    DBSession.add(pds)
    DBSession.flush()

    return pds

def add_Graph(name, template='graph', vlabel='vlabel'):
    graph = tables.Graph(
        name=u'' + name,
        template=u'' + template,
        vlabel=u'' + vlabel,
    )
    DBSession.add(graph)
    DBSession.flush()
    return graph

def add_Graph2GraphGroup(graph, group):
    if isinstance(group, basestring):
        group = tables.GraphGroup.by_group_name(u'' + group)

    if isinstance(graph, basestring):
        graph = tables.Graph.by_graph_name(u'' + graph)

    group.graphs.append(graph)
    DBSession.flush()

def add_PerfDataSource2Graph(source, graph):
    if isinstance(graph, basestring):
        graph = tables.Graph.by_graph_name(u'' + graph)

    if isinstance(source, tuple):
        source = tables.PerfDataSource.by_service_and_source_name(*source)

    graph.perfdatasources.append(source)
    DBSession.flush()

service1 = (u'proto4', u'UpTime')
service2 = (u'proto4', u'Load')
source1 = add_PerfDataSource(service2, 'Load 01')
source2 = add_PerfDataSource(service2, 'Load 05')
source3 = add_PerfDataSource(service2, 'Load 15')
source4 = add_PerfDataSource(service1, 'sysUpTime')

add_Graph('UpTime')
add_Graph('Load')
add_Graph2GraphGroup('UpTime', 'Graphes')
add_Graph2GraphGroup('Load', 'Graphes')
add_PerfDataSource2Graph(source1, 'Load')
add_PerfDataSource2Graph(source2, 'Load')
add_PerfDataSource2Graph(source3, 'Load')
add_PerfDataSource2Graph(source4, 'UpTime')

