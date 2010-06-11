# -*- coding: utf-8 -*-
"""Insère des données de test dans la base de données."""

from vigilo.models.demo.functions import *

def main():
    # Affectation des permissions aux groupes d'utilisateurs.
    managers = tables.UserGroup.by_group_name(u'managers')

    # Host
    add_host('ajc.fw.1')
    add_host('ajc.linux1')
    add_host('ajc.sw.1')
    add_host('bdx.fw.1')
    add_host('bdx.linux1')
    add_host('brouteur')
    add_host('bst.fw.1')
    add_host('bst.unix0')
    add_host('bst.unix1')
    add_host('bst.win0')
    add_host('messagerie')
    add_host('par.fw.1')
    add_host('par.linux0')
    add_host('par.linux1')
    add_host('par.unix0')
    add_host('proto4')
    add_host('server.mails')
    add_host('testaix')
    add_host('testnortel')
    add_host('testsolaris')
    add_host('host1.example.com')
    add_host('host2.example.com')
    add_host('host3.example.com')
    add_host('host4.example.com')
    add_host('host5.example.com')
    add_host('routeur1')
    add_host('routeur2')
    add_host('firewall')
    add_host('localhost')

    # Tags
    add_tag("important", ("messagerie",None))
    add_tag("mco", ("par.linux1", None))
    add_tag("important", ("proto4", None))
    add_tag("security", ("firewall", None))

    # LowLevelService
    add_lowlevelservice('host1.example.com', 'Interface eth0')
    add_lowlevelservice('host2.example.com', 'Interface eth0')
    add_lowlevelservice('host5.example.com', 'Interface eth0')
    add_lowlevelservice('messagerie', 'Interface eth0')
    add_lowlevelservice('routeur1', 'Interface eth0')
    add_lowlevelservice('routeur2', 'Interface eth0')
    add_lowlevelservice('firewall', 'Interface eth0')
    add_lowlevelservice('proto4', 'Interface eth0')
    add_lowlevelservice('host2.example.com', 'Interface eth1', weight=120)
    add_lowlevelservice('host3.example.com', 'Interface eth1')
    add_lowlevelservice('routeur1', 'Interface eth1')
    add_lowlevelservice('routeur2', 'Interface eth1')
    add_lowlevelservice('firewall', 'Interface eth1')
    add_lowlevelservice('host2.example.com', 'Interface eth2', weight=130)
    add_lowlevelservice('brouteur', 'UpTime')
    add_lowlevelservice('messagerie', 'UpTime')
    add_lowlevelservice('proto4', 'UpTime')
    add_lowlevelservice('host1.example.com', 'UpTime')
    add_lowlevelservice('host2.example.com', 'UpTime')
    add_lowlevelservice('brouteur', 'CPU')
    add_lowlevelservice('messagerie', 'CPU')
    add_lowlevelservice('proto4', 'CPU')
    add_lowlevelservice('host1.example.com', 'CPU')
    add_lowlevelservice('host2.example.com', 'CPU')
    add_lowlevelservice('brouteur', 'Load')
    add_lowlevelservice('proto4', 'Load')
    add_lowlevelservice('messagerie', 'Load')
    add_lowlevelservice('host1.example.com', 'Load')
    add_lowlevelservice('host2.example.com', 'Load')
    add_lowlevelservice('host4.example.com', 'Load')
    add_lowlevelservice('brouteur', 'Processes')
    add_lowlevelservice('messagerie', 'Processes')
    add_lowlevelservice('proto4', 'Processes')
    add_lowlevelservice('host1.example.com', 'Processes')
    add_lowlevelservice('host2.example.com', 'Processes')
    add_lowlevelservice('host1.example.com', 'HTTPD')
    add_lowlevelservice('host2.example.com', 'HTTPD')
    add_lowlevelservice('messagerie', 'RAM')
    add_lowlevelservice('proto4', 'RAM')
    add_lowlevelservice('brouteur', 'RAM')
    add_lowlevelservice('host1.example.com', 'RAM')
    add_lowlevelservice('host2.example.com', 'RAM')
    add_lowlevelservice('localhost', 'perfdatasource')
    add_lowlevelservice('localhost', 'SSH')
    add_lowlevelservice('localhost', 'HTTP')
    add_lowlevelservice('localhost', 'Root Partition')
    add_lowlevelservice('localhost', 'Swap Usage')

    # HighLevelService
    add_highlevelservice("Connexion", op_dep="+",
                         message="Ouch", priority=3)
    add_highlevelservice("Portail web", op_dep="&",
                         message="Ouch", priority=1)

    # State
    add_svc_state(("host5.example.com", "Interface eth0"), "CRITICAL", "eth0 is down")
    add_svc_state(("host4.example.com", "Load"), "WARNING", "Load reached a warning level")

    # Dependency
    add_dependency((None, 'Connexion'), ('host2.example.com', 'Interface eth0'))
    add_dependency((None, 'Connexion'), ('host2.example.com', 'Interface eth1'))
    add_dependency((None, 'Connexion'), ('host2.example.com', 'Interface eth2'))
    add_dependency((None, 'Portail web'), (None, 'Connexion'))
    add_dependency((None, 'Portail web'), ('host2.example.com', 'HTTPD'))
    add_dependency(('messagerie', 'Processes'), ('messagerie', 'CPU'))
    add_dependency(('messagerie', 'Processes'), ('messagerie', 'RAM'))
    add_dependency(('messagerie', 'CPU'), ('messagerie', 'Interface eth0'))
    add_dependency(('messagerie', 'RAM'), ('messagerie', 'Interface eth0'))
    add_dependency(('messagerie', 'Interface eth0'), ('routeur1', 'Interface eth1'))
    add_dependency(('messagerie', 'Interface eth0'), ('routeur2', 'Interface eth1'))
    add_dependency(('host1.example.com', 'Processes'), ('host1.example.com', 'CPU'))
    add_dependency(('host1.example.com', 'Processes'), ('host1.example.com', 'RAM'))
    add_dependency(('host1.example.com', 'CPU'), ('host1.example.com', 'Interface eth0'))
    add_dependency(('host1.example.com', 'RAM'), ('host1.example.com', 'Interface eth0'))
    add_dependency(('host1.example.com', 'Interface eth0'), ('firewall', 'Interface eth1'))
    add_dependency(('firewall', 'Interface eth1'), ('firewall', 'Interface eth0'))
    add_dependency(('firewall', 'Interface eth0'), ('routeur1', 'Interface eth1'))
    add_dependency(('firewall', 'Interface eth0'), ('routeur2', 'Interface eth1'))
    add_dependency(('routeur1', 'Interface eth1'), ('routeur1', 'Interface eth0'))
    add_dependency(('routeur2', 'Interface eth1'), ('routeur2', 'Interface eth0'))

    # SupItemGroup
    servers = add_supitemgroup("Serveurs")
    linux = add_supitemgroup("Serveurs Linux")
    windows = add_supitemgroup("Serveurs Windows")
    add_supitemgroup_parent(linux, servers)
    add_supitemgroup_parent(windows, servers)

    # GraphGroup
    graphes = add_graphgroup("Graphes")

    # Affectation des permissions aux groupes d'hôtes.
    add_supitemgrouppermission('Serveurs', 'managers')
    add_supitemgrouppermission('Serveurs Linux', 'managers')
    add_supitemgrouppermission('Serveurs Windows', 'managers')

    # Affectation des hôtes aux groupes d'hôtes.
    add_host2group('ajc.fw.1', 'Serveurs')
    add_host2group('ajc.linux1', 'Serveurs Linux')
    add_host2group('ajc.sw.1', 'Serveurs')
    add_host2group('bdx.fw.1', 'Serveurs')
    add_host2group('bdx.linux1', 'Serveurs Linux')
    add_host2group('brouteur', 'Serveurs')
    add_host2group('bst.fw.1', 'Serveurs')
    add_host2group('bst.unix0', 'Serveurs')
    add_host2group('bst.unix1', 'Serveurs Linux')
    add_host2group('bst.win0', 'Serveurs Windows')
    add_host2group('messagerie', 'Serveurs Linux')
    add_host2group('par.fw.1', 'Serveurs Linux')
    add_host2group('par.linux0', 'Serveurs Linux')
    add_host2group('par.linux1', 'Serveurs Linux')
    add_host2group('par.unix0', 'Serveurs Linux')
    add_host2group('proto4', 'Serveurs Linux')
    add_host2group('server.mails', 'Serveurs Linux')
    add_host2group('testaix', 'Serveurs Windows')
    add_host2group('testnortel', 'Serveurs Windows')
    add_host2group('testsolaris', 'Serveurs Windows')
    add_host2group('host1.example.com', 'Serveurs Linux')
    add_host2group('host2.example.com', 'Serveurs Linux')
    add_host2group('host3.example.com', 'Serveurs Linux')
    add_host2group('routeur1', 'Serveurs Linux')
    add_host2group('routeur2', 'Serveurs Linux')
    add_host2group('firewall', 'Serveurs Linux')
    add_host2group('localhost', 'Serveurs Windows')

    # Affectation des services aux groupes de services
    add_lls2group(('localhost', 'SSH'), 'Serveurs Linux')

    # Applications
    add_application('nagios')
    add_application('rrdgraph')
    add_application('collector')
    add_application('connector-nagios')

    # VigiloServer
    add_vigiloserver('localhost')

    # Ventilation
    # add_ventilation(h1, h2, app)
    # L'appli app pour h1 se trouve sur h2.
    add_ventilation('localhost', 'localhost', 'rrdgraph')
    add_ventilation('localhost', 'localhost', 'nagios')
    add_ventilation('proto4', 'localhost', 'rrdgraph')

    # Métrologie
    service1 = ('proto4', 'UpTime')
    service2 = ('proto4', 'Load')
    service3 = ('proto4', 'Interface eth0')
    source1 = add_perfdatasource('Load 01', 'proto4')
    source2 = add_perfdatasource('Load 05', 'proto4')
    source3 = add_perfdatasource('Load 15', 'proto4')
    source4 = add_perfdatasource('sysUpTime', 'proto4')
    source4 = add_perfdatasource('ineth0', 'proto4', max=512000)
    source4 = add_perfdatasource('outeth0', 'proto4', max=512000)

    graph_UpTime = add_graph('UpTime')
    graph_Load = add_graph('Load')
    add_graph2group(graph_UpTime, 'Graphes')
    add_graph2group(graph_Load, 'Graphes')
    add_perfdatasource2graph(source1, graph_Load)
    add_perfdatasource2graph(source2, graph_Load)
    add_perfdatasource2graph(source3, graph_Load)
    add_perfdatasource2graph(source4, graph_UpTime)

    # Cartographie
    add_mapgroup('Groupe 1', 'Root')
    add_mapgroup('Groupe 1.1', 'Groupe 1')
    add_mapgroup('Groupe 1.2', 'Groupe 1')
    add_mapgroup('Groupe 2', 'Root')
    add_mapgroup('Groupe 2.1', 'Groupe 2')
    add_mapgroup('Groupe 1.1.1', 'Groupe 1.1')
    add_mapgroup('Groupe 1.1.1.1', 'Groupe 1.1.1')
    add_mapgroup('Groupe 3', 'Root')

    maps = []
    for i in range(1, 4):
        m = add_map("Carte %d" % i)
        maps.append(m)
    add_map2group(maps[0], 'Groupe 1')
    add_map2group(maps[1], 'Groupe 1.1')
    add_map2group(maps[2], 'Groupe 1.1')
    add_map2group(maps[0], 'Groupe 2.1')
    add_map2group(maps[1], 'Groupe 2.1')
    add_map2group(maps[2], 'Groupe 2.1')

    #n1 = add_node_host("host1.example.com", 'Host 1', maps[0], "ServiceElement", 220, 350, 'server', maps[0:3])
    n1 = add_node_host("proto4", 'Proto 4', maps[0], "ServiceElement", 220, 350, 'server', maps[0:3])
    n2 = add_node_host("host2.example.com", 'Host 2', maps[0], "ServiceElement", 350, 140, 'firewall', maps[0:2])
    n3 = add_node_host("host3.example.com", 'Host 3', maps[0], "ServiceElement", 350, 250, 'switch', maps[0:2])
    n4 = add_node_host("host4.example.com", 'Host 4', maps[0], "ServiceElement", 590, 140, 'router', maps[0:2])
    n5 = add_node_host("host5.example.com", 'Host 5', maps[0], "ServiceElement", 480, 350, 'server', maps[0:2])

    n6 = add_node_lls(('host1.example.com', 'Interface eth0'), "Internet", maps[0], "ServiceElement", 590, 350, 'network-cloud', maps[0:3])

    l1 = add_mapllslink(n1, n3, ('proto4', 'Interface eth0'), maps[0])
    l2 = add_mapllslink(n2, n3, ('host1.example.com', 'Interface eth0'), maps[0])
    l3 = add_mapllslink(n4, n2, ('host1.example.com', 'Interface eth0'), maps[0])
    l4 = add_mapllslink(n5, n3, ('host1.example.com', 'Interface eth0'), maps[0])
    l5 = add_mapllslink(n5, n1, ('host1.example.com', 'Interface eth0'), maps[0])
    l6 = add_mapllslink(n4, n6, ('host1.example.com', 'Interface eth0'), maps[0])

    # Ajout des l'utilisateur 'editor' et 'reader' avec des permissions limitées.
    # Utilisé pour vérifier la gestion des permissions.
    add_user('editor', u'editor@somedomain.com', u'Editor', u'editpass', 'editors')
    add_usergroup_permission('editors', 'vigimap-access')
    add_usergroup_permission('editors', 'vigimap-edit')
    
    add_user('reader', u'reader@somedomain.com', u'Reader', u'readpass', 'readers')
    add_usergroup_permission('readers', 'vigimap-access')

    add_MapGroupPermission('Groupe 1', 'managers', 'r')
    add_MapGroupPermission('Groupe 2', 'managers', 'w')
    add_MapGroupPermission('Groupe 3', 'managers', 'r')
    add_MapGroupPermission('Groupe 1', 'editors', 'w')
    add_MapGroupPermission('Groupe 3', 'editors', 'w')
    add_MapGroupPermission('Groupe 1', 'readers', 'r')


