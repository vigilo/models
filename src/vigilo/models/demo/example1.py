# -*- coding: utf-8 -*-
# Copyright (C) 2006-2014 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Insère des données de test dans la base de données."""

# pylint: disable-msg=W0612
# W0612: Unused variables

from vigilo.models.demo import functions
from vigilo.models import tables

def main():
    """
    Scénario de démonstration n°1.
    Peut être invoqué à l'aide de la commande C{vigilo-models-demo}.
    """

    # Affectation des permissions aux groupes d'utilisateurs.
    managers = tables.UserGroup.by_group_name(u'managers')

    # Host
    functions.add_host('ajc.fw.1')
    functions.add_host('ajc.linux1')
    functions.add_host('ajc.sw.1')
    functions.add_host('bdx.fw.1')
    functions.add_host('bdx.linux1')
    functions.add_host('brouteur')
    functions.add_host('bst.fw.1')
    functions.add_host('bst.unix0')
    functions.add_host('bst.unix1')
    functions.add_host('bst.win0')
    functions.add_host('messagerie')
    functions.add_host('par.fw.1')
    functions.add_host('par.linux0')
    functions.add_host('par.linux1')
    functions.add_host('par.unix0')
    functions.add_host('proto4')
    functions.add_host('server.mails')
    functions.add_host('testaix')
    functions.add_host('testnortel')
    functions.add_host('testsolaris')
    functions.add_host('host1.example.com')
    functions.add_host('host2.example.com')
    functions.add_host('host3.example.com')
    functions.add_host('host4.example.com')
    functions.add_host('host5.example.com')
    functions.add_host('routeur1')
    functions.add_host('routeur2')
    functions.add_host('firewall')
    functions.add_host('localhost')
    functions.add_host('shows.how.vigigraph.may.make.an.ellipse')

    # Tags
    functions.add_tag(("messagerie", None), "important")
    functions.add_tag(("par.linux1", None), "mco")
    functions.add_tag(("proto4", None), "important")
    functions.add_tag(("firewall", None), "security")

    # LowLevelService
    functions.add_lowlevelservice('host1.example.com', 'Interface eth0')
    functions.add_lowlevelservice('host2.example.com', 'Interface eth0')
    functions.add_lowlevelservice('host5.example.com', 'Interface eth0')
    functions.add_lowlevelservice('messagerie', 'Interface eth0')
    functions.add_lowlevelservice('routeur1', 'Interface eth0')
    functions.add_lowlevelservice('routeur2', 'Interface eth0')
    functions.add_lowlevelservice('firewall', 'Interface eth0')
    functions.add_lowlevelservice('proto4', 'Interface eth0')
    functions.add_lowlevelservice('host2.example.com', 'Interface eth1',
                                    weight=120)
    functions.add_lowlevelservice('host3.example.com', 'Interface eth1')
    functions.add_lowlevelservice('routeur1', 'Interface eth1')
    functions.add_lowlevelservice('routeur2', 'Interface eth1')
    functions.add_lowlevelservice('firewall', 'Interface eth1')
    functions.add_lowlevelservice('host2.example.com', 'Interface eth2',
                                    weight=130)
    functions.add_lowlevelservice('brouteur', 'UpTime')
    functions.add_lowlevelservice('messagerie', 'UpTime')
    functions.add_lowlevelservice('proto4', 'UpTime')
    functions.add_lowlevelservice('host1.example.com', 'UpTime')
    functions.add_lowlevelservice('host2.example.com', 'UpTime')
    functions.add_lowlevelservice('brouteur', 'CPU')
    functions.add_lowlevelservice('messagerie', 'CPU')
    functions.add_lowlevelservice('proto4', 'CPU')
    functions.add_lowlevelservice('host1.example.com', 'CPU')
    functions.add_lowlevelservice('host2.example.com', 'CPU')
    functions.add_lowlevelservice('brouteur', 'Load')
    functions.add_lowlevelservice('proto4', 'Load')
    functions.add_lowlevelservice('messagerie', 'Load')
    functions.add_lowlevelservice('host1.example.com', 'Load')
    functions.add_lowlevelservice('host2.example.com', 'Load')
    functions.add_lowlevelservice('host4.example.com', 'Load')
    functions.add_lowlevelservice('brouteur', 'Processes')
    functions.add_lowlevelservice('messagerie', 'Processes')
    functions.add_lowlevelservice('proto4', 'Processes')
    functions.add_lowlevelservice('host1.example.com', 'Processes')
    functions.add_lowlevelservice('host2.example.com', 'Processes')
    functions.add_lowlevelservice('host1.example.com', 'HTTPD')
    functions.add_lowlevelservice('host2.example.com', 'HTTPD')
    functions.add_lowlevelservice('messagerie', 'RAM')
    functions.add_lowlevelservice('proto4', 'RAM')
    functions.add_lowlevelservice('brouteur', 'RAM')
    functions.add_lowlevelservice('host1.example.com', 'RAM')
    functions.add_lowlevelservice('host2.example.com', 'RAM')
    functions.add_lowlevelservice('localhost', 'perfdatasource')
    functions.add_lowlevelservice('localhost', 'SSH')
    functions.add_lowlevelservice('localhost', 'HTTP')
    functions.add_lowlevelservice('localhost', 'Root Partition')
    functions.add_lowlevelservice('localhost', 'Swap Usage')

    # HighLevelService
    functions.add_highlevelservice(
        "Connexion",
        message="Ouch",
        priorities={
            u'UNKNOWN': 3,
            u'WARNING': 3,
            u'CRITICAL': 3,
        })
    functions.add_highlevelservice("Portail web", message="Ouch")

    # State
    functions.add_svc_state(
        ("host5.example.com", "Interface eth0"),
        "CRITICAL",
        "eth0 is down")
    functions.add_svc_state(
        ("host4.example.com", "Load"),
        "WARNING",
        "Load reached a warning level")

    # DependencyGroup
    host1 = 'host1.example.com'
    depgroup_connexion = \
        functions.add_dependency_group(None, 'Connexion', 'hls', '&')
    depgroup_portail = \
        functions.add_dependency_group(None, 'Portail web', 'hls', '&')
    depgroup_processes = \
        functions.add_dependency_group(
            'messagerie', 'Processes', 'topology', '&')
    depgroup_cpu = \
        functions.add_dependency_group('messagerie', 'CPU', 'topology', '&')
    depgroup_ram = \
        functions.add_dependency_group('messagerie', 'RAM', 'topology', '&')
    depgroup_eth = \
        functions.add_dependency_group(
            'messagerie', 'Interface eth0', 'topology', '&')
    depgroup_processes2 = \
        functions.add_dependency_group(host1, 'Processes', 'topology', '&')
    depgroup_cpu2 = \
        functions.add_dependency_group(host1, 'CPU', 'topology', '&')
    depgroup_ram2 = \
        functions.add_dependency_group(host1, 'RAM', 'topology', '&')
    depgroup_eth2 = \
        functions.add_dependency_group(host1, 'Interface eth0', 'topology', '&')
    depgroup_eth3 = \
        functions.add_dependency_group(
            'firewall', 'Interface eth1', 'topology', '&')
    depgroup_eth4 = \
        functions.add_dependency_group(
            'firewall', 'Interface eth0', 'topology', '&')
    depgroup_eth5 = \
        functions.add_dependency_group(
            'routeur1', 'Interface eth1', 'topology', '&')
    depgroup_eth6 = \
        functions.add_dependency_group(
            'routeur2', 'Interface eth1', 'topology', '&')

    # Dependency
    functions.add_dependency(
        depgroup_connexion, ('host2.example.com', 'Interface eth0'))
    functions.add_dependency(
        depgroup_connexion, ('host2.example.com', 'Interface eth1'))
    functions.add_dependency(
        depgroup_connexion, ('host2.example.com', 'Interface eth2'))
    functions.add_dependency(depgroup_portail, (None, 'Connexion'))
    functions.add_dependency(depgroup_portail, ('host2.example.com', 'HTTPD'))
    functions.add_dependency(depgroup_processes, ('messagerie', 'CPU'))
    functions.add_dependency(depgroup_processes, ('messagerie', 'RAM'))
    functions.add_dependency(depgroup_cpu, ('messagerie', 'Interface eth0'))
    functions.add_dependency(depgroup_ram, ('messagerie', 'Interface eth0'))
    functions.add_dependency(depgroup_eth, ('routeur1', 'Interface eth1'))
    functions.add_dependency(depgroup_eth, ('routeur2', 'Interface eth1'))
    functions.add_dependency(depgroup_processes2, ('host1.example.com', 'CPU'))
    functions.add_dependency(depgroup_processes2, ('host1.example.com', 'RAM'))
    functions.add_dependency(
        depgroup_cpu2, ('host1.example.com', 'Interface eth0'))
    functions.add_dependency(
        depgroup_ram2, ('host1.example.com', 'Interface eth0'))
    functions.add_dependency(depgroup_eth2, ('firewall', 'Interface eth1'))
    functions.add_dependency(depgroup_eth3, ('firewall', 'Interface eth0'))
    functions.add_dependency(depgroup_eth4, ('routeur1', 'Interface eth1'))
    functions.add_dependency(depgroup_eth4, ('routeur2', 'Interface eth1'))
    functions.add_dependency(depgroup_eth5, ('routeur1', 'Interface eth0'))
    functions.add_dependency(depgroup_eth6, ('routeur2', 'Interface eth0'))

    # SupItemGroup
    servers = functions.add_supitemgroup("Serveurs")
    linux = functions.add_supitemgroup("Serveurs Linux")
    windows = functions.add_supitemgroup("Serveurs Windows")
    functions.add_supitemgroup_parent(linux, servers)
    functions.add_supitemgroup_parent(windows, servers)

    # GraphGroup
    graphes = functions.add_graphgroup("Graphes")

    # Affectation des permissions aux groupes d'hôtes.
    functions.add_supitemgrouppermission('Serveurs', 'managers')
    functions.add_supitemgrouppermission('Serveurs Linux', 'managers')
    functions.add_supitemgrouppermission('Serveurs Windows', 'managers')

    # Affectation des hôtes aux groupes d'hôtes.
    functions.add_host2group('ajc.fw.1', 'Serveurs')
    functions.add_host2group('ajc.linux1', 'Serveurs Linux')
    functions.add_host2group('ajc.sw.1', 'Serveurs')
    functions.add_host2group('bdx.fw.1', 'Serveurs')
    functions.add_host2group('bdx.linux1', 'Serveurs Linux')
    functions.add_host2group('brouteur', 'Serveurs')
    functions.add_host2group('bst.fw.1', 'Serveurs')
    functions.add_host2group('bst.unix0', 'Serveurs')
    functions.add_host2group('bst.unix1', 'Serveurs Linux')
    functions.add_host2group('bst.win0', 'Serveurs Windows')
    functions.add_host2group('messagerie', 'Serveurs Linux')
    functions.add_host2group('par.fw.1', 'Serveurs Linux')
    functions.add_host2group('par.linux0', 'Serveurs Linux')
    functions.add_host2group('par.linux1', 'Serveurs Linux')
    functions.add_host2group('par.unix0', 'Serveurs Linux')
    functions.add_host2group('proto4', 'Serveurs Linux')
    functions.add_host2group(
        'shows.how.vigigraph.may.make.an.ellipse', 'Serveurs Linux')
    functions.add_host2group('server.mails', 'Serveurs Linux')
    functions.add_host2group('testaix', 'Serveurs Windows')
    functions.add_host2group('testnortel', 'Serveurs Windows')
    functions.add_host2group('testsolaris', 'Serveurs Windows')
    functions.add_host2group('host1.example.com', 'Serveurs Linux')
    functions.add_host2group('host2.example.com', 'Serveurs Linux')
    functions.add_host2group('host3.example.com', 'Serveurs Linux')
    functions.add_host2group('routeur1', 'Serveurs Linux')
    functions.add_host2group('routeur2', 'Serveurs Linux')
    functions.add_host2group('firewall', 'Serveurs Linux')
    functions.add_host2group('localhost', 'Serveurs Windows')

    # Affectation des services aux groupes de services
    functions.add_lls2group(('localhost', 'SSH'), 'Serveurs Linux')

    # Applications
    functions.add_application('nagios')
    functions.add_application('vigirrd')
    functions.add_application('collector')
    functions.add_application('connector-nagios')

    # VigiloServer
    functions.add_vigiloserver('localhost')

    # Ventilation
    # add_ventilation(h1, h2, app)
    # L'appli app pour h1 se trouve sur h2.
    functions.add_ventilation('localhost', 'localhost', 'vigirrd')
    functions.add_ventilation('localhost', 'localhost', 'nagios')
    functions.add_ventilation('proto4', 'localhost', 'vigirrd')
    functions.add_ventilation('shows.how.vigigraph.may.make.an.ellipse',
                    'localhost', 'vigirrd')

    # Métrologie
    service1 = ('proto4', 'UpTime')
    service2 = ('proto4', 'Load')
    service3 = ('proto4', 'Interface eth0')
    service4 = ('shows.how.vigigraph.may.make.an.ellipse', 'UpTime')
    source1 = functions.add_perfdatasource('Load 01', 'proto4')
    source2 = functions.add_perfdatasource('Load 05', 'proto4')
    source3 = functions.add_perfdatasource('Load 15', 'proto4')
    source4 = functions.add_perfdatasource('sysUpTime', 'proto4')
    source5 = functions.add_perfdatasource('sysUpTime',
        'shows.how.vigigraph.may.make.an.ellipse')
    source6 = functions.add_perfdatasource('ineth0', 'proto4', max=512000)
    source7 = functions.add_perfdatasource('outeth0', 'proto4', max=512000)

    graph_UpTime = functions.add_graph('UpTime')
    graph_Load = functions.add_graph('Load')
    graph_UpTime2 = functions.add_graph('UpTime')
    functions.add_graph2group(graph_UpTime, 'Graphes')
    functions.add_graph2group(graph_Load, 'Graphes')
    functions.add_graph2group(graph_UpTime2, 'Graphes')
    functions.add_perfdatasource2graph(source1, graph_Load)
    functions.add_perfdatasource2graph(source2, graph_Load)
    functions.add_perfdatasource2graph(source3, graph_Load)
    functions.add_perfdatasource2graph(source4, graph_UpTime)
    functions.add_perfdatasource2graph(source5, graph_UpTime2)

    # Cartographie
    mg_root = functions.add_mapgroup('Root', None)
    mg_1 = functions.add_mapgroup('Groupe 1', mg_root)
    mg_1_1 = functions.add_mapgroup('Groupe 1.1', mg_1)
    mg_1_2 = functions.add_mapgroup('Groupe 1.2', mg_1)
    mg_2 = functions.add_mapgroup('Groupe 2', mg_root)
    mg_2_1 = functions.add_mapgroup('Groupe 2.1', mg_2)
    mg_1_1_1 = functions.add_mapgroup('Groupe 1.1.1', mg_1_1)
    mg_1_1_1_1 = functions.add_mapgroup('Groupe 1.1.1.1', mg_1_1_1)
    mg_3 = functions.add_mapgroup('Groupe 3', mg_root)

    maps = []
    for i in range(1, 4):
        m = functions.add_map("Carte %d" % i)
        maps.append(m)
    functions.add_map2group(maps[0], mg_1)
    functions.add_map2group(maps[1], mg_1_1)
    functions.add_map2group(maps[2], mg_1_1)
    functions.add_map2group(maps[0], mg_2_1)
    functions.add_map2group(maps[1], mg_2_1)
    functions.add_map2group(maps[2], mg_2_1)

    n1 = functions.add_node_host(
        "proto4", 'Proto 4', maps[0], "ServiceElement",
        220, 350, 'server', maps[0:3])
    n2 = functions.add_node_host(
        "host2.example.com", 'Host 2', maps[0], "ServiceElement",
        350, 140, 'firewall', maps[0:2])
    n3 = functions.add_node_host(
        "host3.example.com", 'Host 3', maps[0], "ServiceElement",
        350, 250, 'switch', maps[0:2])
    n4 = functions.add_node_host(
        "host4.example.com", 'Host 4', maps[0], "ServiceElement",
        590, 140, 'router', maps[0:2])
    n5 = functions.add_node_host(
        "host5.example.com", 'Host 5', maps[0], "ServiceElement",
        480, 350, 'server', maps[0:2])

    n6 = functions.add_node_lls(
        ('host1.example.com', 'Interface eth0'),
        "Internet", maps[0], "ServiceElement",
        590, 350, 'network-cloud', maps[0:3])

    service = ('host1.example.com', 'Interface eth0')
    l1 = functions.add_mapllslink(n1, n3, ('proto4', 'Interface eth0'), maps[0])
    l2 = functions.add_mapllslink(n2, n3, service, maps[0])
    l3 = functions.add_mapllslink(n4, n2, service, maps[0])
    l4 = functions.add_mapllslink(n5, n3, service, maps[0])
    l5 = functions.add_mapllslink(n5, n1, service, maps[0])
    l6 = functions.add_mapllslink(n4, n6, service, maps[0])

    # Ajout des groupes d'utilisateurs 'editors' et 'readers'.
    functions.add_usergroup('editors')
    functions.add_usergroup('readers')

    # Ajout des utilisateurs 'editor' et 'reader' avec des permissions limitées.
    # Utilisé pour vérifier la gestion des permissions.
    functions.add_user('editor', u'editor@somedomain.com',
        u'Editor', u'editpass', 'editors')
    functions.add_usergroup_permission('editors', 'vigimap-access')
    functions.add_usergroup_permission('editors', 'vigimap-edit')

    functions.add_user('reader', u'reader@somedomain.com',
        u'Reader', u'readpass', 'readers')
    functions.add_usergroup_permission('readers', 'vigimap-access')

    functions.add_MapGroupPermission(mg_1, 'managers', 'r')
    functions.add_MapGroupPermission(mg_2, 'managers', 'w')
    functions.add_MapGroupPermission(mg_3, 'managers', 'r')
    functions.add_MapGroupPermission(mg_1, 'editors', 'w')
    functions.add_MapGroupPermission(mg_3, 'editors', 'w')
    functions.add_MapGroupPermission(mg_1, 'readers', 'r')
