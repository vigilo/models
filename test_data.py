# -*- coding: utf-8 -*-
"""Insère des données de test dans la base de données."""

import atexit
from vigilo.models.session import DBSession
from vigilo import models

def commit_on_exit():
    """
    Effectue un COMMIT sur la transaction à la fin de l'exécution
    du script d'insertion des données de test.
    """
    import transaction
    transaction.commit()
atexit.register(commit_on_exit)

# Noms des états
DBSession.add(models.StateName(statename=u'OK', order=0))
DBSession.add(models.StateName(statename=u'UNKNOWN', order=1))
DBSession.add(models.StateName(statename=u'WARNING', order=2))
DBSession.add(models.StateName(statename=u'CRITICAL', order=3))
DBSession.add(models.StateName(statename=u'UP', order=0))
DBSession.add(models.StateName(statename=u'UNREACHABLE', order=1))
DBSession.add(models.StateName(statename=u'DOWN', order=3))
DBSession.flush()

# Etats possibles de la mise en silence pour maintenance
DBSession.add(models.DowntimeStatus(status=u'Planified',))
DBSession.add(models.DowntimeStatus(status=u'Enabled',))
DBSession.add(models.DowntimeStatus(status=u'Finished',))
DBSession.add(models.DowntimeStatus(status=u'Cancelled',))
DBSession.flush()

# Permissions
collect = models.Permission(
    permission_name=u'collect',
    description=u'Autorise les utilisateurs à lancer une demande de collecte',
)
DBSession.add(collect)
downtime = models.Permission(
    permission_name=u'downtime',
    description=u'Autorise les utilisateurs à planifier une maintenance',
)
DBSession.add(downtime)
DBSession.flush()

# Affectation des permissions aux groupes d'utilisateurs.
managers = models.UserGroup.by_group_name(u'managers')
managers.permissions.append(collect)
managers.permissions.append(downtime)

# Host
def add_Host(name):
    name = u'' + name

    DBSession.add(models.Host(
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

# ServiceLowLevel
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
        host = models.Host.by_host_name(u'' + hostident)
        kwargs['host'] = host
    else:
        kwargs['host'] = hostident

    DBSession.add(models.ServiceLowLevel(**kwargs))
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
add_LowLevelService('CPU', 'brouteur')
add_LowLevelService('CPU', 'messagerie')
add_LowLevelService('CPU', 'proto4')
add_LowLevelService('CPU', 'host1.example.com')
add_LowLevelService('Load', 'host1.example.com')
add_LowLevelService('Processes', 'brouteur')
add_LowLevelService('Processes', 'messagerie')
add_LowLevelService('Processes', 'proto4')
add_LowLevelService('Processes', 'host1.example.com')
add_LowLevelService('HTTPD', 'host1.example.com')
add_LowLevelService('HTTPD', 'host2.example.com')
add_LowLevelService('RAM', 'messagerie')
add_LowLevelService('RAM', 'host1.example.com')

# ServiceHighLevel
DBSession.add(models.ServiceHighLevel(
    servicename=u'Connexion',
    op_dep=u'+',
    message=u'Ouch',
    warning_threshold=300,
    critical_threshold=150,
    weight=None,
    priority=3,
))
DBSession.flush()

DBSession.add(models.ServiceHighLevel(
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
                models.ServiceHighLevel.by_service_name(u'' + service)
        elif service is None:   # Host
            kwargs['supitem1'] = models.Host.by_host_name(u'' + host)
        else:                   # LLS
            kwargs['supitem1'] = \
                models.ServiceLowLevel.by_host_service_name(
                    u'' + host, u'' + service)

    if isinstance(depended, int):
        kwargs['idsupitem2'] = depended
    else:
        host, service = depended
        if host is None:        # HLS
            kwargs['supitem2'] = \
                models.ServiceHighLevel.by_service_name(u'' + service)
        elif service is None:   # Host
            kwargs['supitem2'] = models.Host.by_host_name(u'' + host)
        else:                   # LLS
            kwargs['supitem2'] = \
                models.ServiceLowLevel.by_host_service_name(
                    u'' + host, u'' + service)

    DBSession.add(models.Dependency(**kwargs))
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

# HostGroup
servers = models.HostGroup(
    name=u'Serveurs',
    parent=None,
)
DBSession.add(servers)
DBSession.flush()

DBSession.add(models.HostGroup(
    name=u'Serveurs Linux',
    parent=servers,
))
DBSession.flush()

DBSession.add(models.HostGroup(
    name=u'Serveurs Windows',
    parent=servers,
))
DBSession.flush()

# ServiceGroup
DBSession.add(models.ServiceGroup(
    name=u'Services',
    parent=None,
))
DBSession.flush()

# Affectation des permissions aux groupes d'hôtes.
def add_HostGroupPermission(group, perm):
    if isinstance(group, basestring):
        group = models.HostGroup.by_group_name(u'' + group)

    if isinstance(perm, basestring):
        perm = models.Permission.by_permission_name(u'' + perm)

    group.permissions.append(perm)
    DBSession.flush()

add_HostGroupPermission('Serveurs', 'edit')
add_HostGroupPermission('Serveurs Linux', 'manage')

# Affectation des permissions aux groupes de services.
def add_ServiceGroupPermission(group, perm):
    if isinstance(group, basestring):
        group = models.ServiceGroup.by_group_name(u'' + group)

    if isinstance(perm, basestring):
        perm = models.Permission.by_permission_name(u'' + perm)

    group.permissions.append(perm)
    DBSession.flush()

add_ServiceGroupPermission('Services', 'edit')
add_ServiceGroupPermission('Services', 'manage')

# Affectation des hôtes aux groupes d'hôtes.
def add_Host2HostGroup(host, group):
    if isinstance(group, basestring):
        group = models.HostGroup.by_group_name(u'' + group)

    if isinstance(host, basestring):
        host = models.Host.by_host_name(u'' + host)

    group.hosts.append(host)
    DBSession.flush()

add_Host2HostGroup('ajc.fw.1', 'Serveurs')
add_Host2HostGroup('ajc.linux1', 'Serveurs')
add_Host2HostGroup('ajc.sw.1', 'Serveurs')
add_Host2HostGroup('bdx.fw.1', 'Serveurs')
add_Host2HostGroup('bdx.linux1', 'Serveurs')
add_Host2HostGroup('brouteur', 'Serveurs')
add_Host2HostGroup('bst.fw.1', 'Serveurs')
add_Host2HostGroup('bst.unix0', 'Serveurs')
add_Host2HostGroup('bst.unix1', 'Serveurs')
add_Host2HostGroup('bst.win0', 'Serveurs Linux')
add_Host2HostGroup('messagerie', 'Serveurs Linux')
add_Host2HostGroup('par.fw.1', 'Serveurs Linux')
add_Host2HostGroup('par.linux0', 'Serveurs Linux')
add_Host2HostGroup('par.linux1', 'Serveurs Linux')
add_Host2HostGroup('par.unix0', 'Serveurs Linux')
add_Host2HostGroup('proto4', 'Serveurs Linux')
add_Host2HostGroup('server.mails', 'Serveurs Linux')
add_Host2HostGroup('testaix', 'Serveurs Linux')
add_Host2HostGroup('testnortel', 'Serveurs Linux')
add_Host2HostGroup('testsolaris', 'Serveurs Linux')
add_Host2HostGroup('host1.example.com', 'Serveurs Linux')
add_Host2HostGroup('host2.example.com', 'Serveurs Linux')
add_Host2HostGroup('host3.example.com', 'Serveurs Linux')
add_Host2HostGroup('routeur1', 'Serveurs Linux')
add_Host2HostGroup('routeur2', 'Serveurs Linux')
add_Host2HostGroup('firewall', 'Serveurs Linux')

# Affectation des services aux groupes de services.
def add_Service2ServiceGroup(lls, group):
    if isinstance(group, basestring):
        group = models.ServiceGroup.by_group_name(u'' + group)

    if isinstance(lls, tuple):
        host, service = lls
        lls = models.ServiceLowLevel.by_host_service_name(
            u'' + host, u'' + service)

    group.services.append(lls)
    DBSession.flush()

add_Service2ServiceGroup(('brouteur', 'UpTime'), 'Services')
add_Service2ServiceGroup(('brouteur', 'CPU'), 'Services')
add_Service2ServiceGroup(('brouteur', 'Processes'), 'Services')
add_Service2ServiceGroup(('firewall', 'Interface eth0'), 'Services')
add_Service2ServiceGroup(('firewall', 'Interface eth1'), 'Services')
add_Service2ServiceGroup(('host1.example.com', 'CPU'), 'Services')
add_Service2ServiceGroup(('host1.example.com', 'Load'), 'Services')
add_Service2ServiceGroup(('host1.example.com', 'Processes'), 'Services')
add_Service2ServiceGroup(('host1.example.com', 'HTTPD'), 'Services')
add_Service2ServiceGroup(('host1.example.com', 'RAM'), 'Services')
add_Service2ServiceGroup(('host1.example.com', 'Interface eth0'), 'Services')
add_Service2ServiceGroup(('host2.example.com', 'Interface eth0'), 'Services')
add_Service2ServiceGroup(('host2.example.com', 'Interface eth1'), 'Services')
add_Service2ServiceGroup(('host2.example.com', 'Interface eth2'), 'Services')
add_Service2ServiceGroup(('host2.example.com', 'HTTPD'), 'Services')
add_Service2ServiceGroup(('host3.example.com', 'Interface eth1'), 'Services')
add_Service2ServiceGroup(('messagerie', 'CPU'), 'Services')
add_Service2ServiceGroup(('messagerie', 'Interface eth0'), 'Services')
add_Service2ServiceGroup(('messagerie', 'Processes'), 'Services')
add_Service2ServiceGroup(('messagerie', 'RAM'), 'Services')
add_Service2ServiceGroup(('messagerie', 'UpTime'), 'Services')
add_Service2ServiceGroup(('proto4', 'Processes'), 'Services')
add_Service2ServiceGroup(('proto4', 'UpTime'), 'Services')
add_Service2ServiceGroup(('proto4', 'CPU'), 'Services')
add_Service2ServiceGroup(('routeur1', 'Interface eth0'), 'Services')
add_Service2ServiceGroup(('routeur1', 'Interface eth1'), 'Services')
add_Service2ServiceGroup(('routeur2', 'Interface eth0'), 'Services')
add_Service2ServiceGroup(('routeur2', 'Interface eth1'), 'Services')

# Application
def add_Application(name):
    DBSession.add(models.Application(name=u'' + name))
    DBSession.flush()

add_Application('Nagios')
add_Application('Metrology')

# HostApplication/HostBusApplication
def add_HostApp(host, appserver, app, jid=None):
    kwargs = {}

    if jid:
        kwargs['jid'] = u'' + jid

    if isinstance(host, basestring):
        kwargs['host'] = models.Host.by_host_name(u'' + host)
    elif isinstance(host, int):
        kwargs['idhost'] = host

    if isinstance(appserver, basestring):
        kwargs['appserver'] = models.Host.by_host_name(u'' + appserver)
    elif isinstance(appserver, int):
        kwargs['idappserver'] = appserver

    if isinstance(app, basestring):
        kwargs['application'] = models.Application.by_app_name(u'' + app)
    elif isinstance(app, int):
        kwargs['idapp'] = app

    cls = (models.HostBusApplication, models.HostApplication)[jid is None]
    DBSession.add(cls(**kwargs))
    DBSession.flush()

add_HostApp('host1.example.com', 'proto4', 'Nagios', 'connector-nagios@localhost')
add_HostApp('host2.example.com', 'proto4', 'Nagios', 'connector-nagios@localhost')
add_HostApp('host3.example.com', 'proto4', 'Nagios', 'connector-nagios@localhost')
add_HostApp('host2.example.com', 'proto4', 'Metrology')

