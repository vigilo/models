# -*- coding: utf-8 -*-
"""
Fonctions permettant de peupler les tables du modèle.
La plupart de ces fonctions tentent d'ajouter un nouvel
élément dans la base de données s'il n'existe pas déjà.
Dans le cas où l'élément existe déjà, il est retourné
intact.
"""

from datetime import datetime

from vigilo.models.session import DBSession
from vigilo.models import tables

#
# Base
#

def add_host(hostname):
    """
    Ajoute un hôte.

    @param hostname: Le nom de l'hôte à ajouter.
    @type hostname: C{basestr}
    @return: Instance de l'hôte créée ou existante.
    @rtype: L{tables.Host}
    """
    h = tables.Host.by_host_name(unicode(hostname))
    if not h:
        h = tables.Host(
                name=unicode(hostname),
                checkhostcmd=u'dummy',
                hosttpl=u'dummy',
                address=u"127.0.0.1",
                snmpcommunity=u"public",
                snmpport=161,
                weight=0)
        DBSession.add(h)
        DBSession.flush()
    return h

def add_lowlevelservice(host, servicename, statename="OK",
                        message="", weight=100):
    """
    Ajoute un service de bas niveau sur un hôte.

    @param host: Nom ou instance d'hôte.
    @type host: C{basestr} ou L{tables.Host}
    @param servicename: Nom du service à créer sur cet hôte.
    @type servicename: C{basestr}
    @param statename: État initial du service.
    @type statename: C{basestr}
    @param message: Message associé à l'état initial du service.
    @type message: C{basestr}
    @param weight: Poids associé au service.
    @type weight: C{int}
    @return: Instance du service créée ou existante.
    @rtype: L{tables.LowLevelService}
    """
    if isinstance(host, basestring):
        hostname = host
        host = tables.Host.by_host_name(unicode(hostname))
        if not host:
            raise ValueError("Invalid host: %s" % hostname)
    servicename = unicode(servicename)
    s = tables.LowLevelService.by_host_service_name(host.name, servicename)
    if not s:
        s = tables.LowLevelService(
                servicename=servicename,
                idhost=host.idhost,
                #servicetype=u"normal",
                #priority=1,
                weight=weight,
                command=u"dummy")
        DBSession.add(s)
        DBSession.flush()
        add_svc_state((host.name, servicename), statename, message)
    return s

def add_highlevelservice(servicename, operator="&", message="", priority=1):
    """
    Ajoute un service de haut niveau.

    @param servicename: Nom du service de haut niveau à ajouter.
    @type servicename: C{basestr}
    @param operator: Opérateur de dépendance ("+", "|" ou "&").
    @type operator: C{basestr}
    @param message: Message qui sera envoyé à Nagios lorsque l'état de
        ce service de haut niveau change. Il peut contenir des formats.
    @type message: C{basestr}
    @param priority: Priorité associée à ce service de haut niveau.
    @type priority: C{int}
    @return: Instance du service de haut niveau créée ou existante.
    @rtype: L{tables.HighLevelService}
    """
    servicename = unicode(servicename)
    s = tables.HighLevelService.by_service_name(servicename)
    if not s:
        # @TODO: traiter l'opérateur de dépendances.
        s = tables.HighLevelService(
                servicename=servicename,
                priority=priority,
                weight=0,
                message=unicode(message),
                warning_threshold=300,
                critical_threshold=150)
        DBSession.add(s)
        DBSession.flush()
    return s

def add_dependency_group(host, service, operator='&'):
    if host is None:        # HLS
        dependent = tables.HighLevelService.by_service_name(unicode(service))
    elif service is None:   # Host
        dependent = tables.Host.by_host_name(unicode(host))
    else:                   # LLS
        dependent = tables.LowLevelService.by_host_service_name(
                        unicode(host), unicode(service))
    group = tables.DependencyGroup(
        operator=unicode(operator),
        dependent=dependent,
    )
    DBSession.add(group)
    DBSession.flush()
    return group.idgroup


def add_dependency(group, depended):
    """
    Ajoute une dépendance à un groupe de dépendances.

    @param group: Groupe de dépendance (identifiant ou instance).
    @type group: C{int} or L{tables.DependencyGroup}
    @param depended: Élément à ajouter au groupe de dépendance,
        sous la forme d'un tuple (hôte, service) décrivant l'élément
        à ajouter.
    @type depended: C{tuple}
    """
    if isinstance(group, int):
        idgroup = group
    else:
        idgroup = group.idgroup

    host, service = depended
    if host is None:        # HLS
        dependency = tables.HighLevelService.by_service_name(unicode(service))
    elif service is None:   # Host
        dependency = tables.Host.by_host_name(unicode(host))
    else:                   # LLS
        dependency = tables.LowLevelService.by_host_service_name(
                        unicode(host), unicode(service))

    DBSession.add(tables.Dependency(
        idgroup=idgroup,
        supitem=dependency,
    ))
    DBSession.flush()


def add_tag(name, supitem=None):
    """
    Ajoute une étiquette (tag), en l'associant éventuellement
    à un élément supervisé existant.

    @param name: Nom de l'étiquette.
    @type name: C{basestr}
    @param supitem: Élément supervisé auquel attacher l'étiquette.
    @type supitem: C{tables.SupItem}
    @return: Instance de l'étiquette créée ou existante.
    @rtype: L{tables.Tag}
    """
    t = tables.Tag.by_tag_name(unicode(name))
    if not t:
        t = tables.Tag(name=unicode(name), value=u"1")
        DBSession.add(t)
        DBSession.flush()
    if supitem is not None:
        add_tag2supitem(t, supitem)
    return t

def add_tag2supitem(tag, supitem):
    """
    Associe une étiquette (tag) à un élément supervisé.

    @param tag: Instance de l'étiquette.
    @type tag: L{tables.Tag}
    @param supitem: Instance de l'élément supervisé ou tuple (hôte, service)
        décrivant l'élément.
    @type supitem: L{tables.SupItem} ou C{tuple}
    """
    if isinstance(supitem, tuple):
        supitem = map(unicode, supitem)
        idsupitem = tables.SupItem.get_supitem(*supitem)
        if not idsupitem:
            return
        supitem = DBSession.query(tables.SupItem).get(idsupitem)
    if tag not in supitem.tags:
        supitem.tags.append(tag)
    DBSession.flush()


#
# Groupes
#

def add_supitemgroup(name, parent=None):
    """
    Ajoute un groupe d'éléments supervisés.

    @param name: Nom du groupe d'éléments supervisés à ajouter.
    @type name: C{basestr}
    @param parent: Parent de ce groupe dans l'arborescence.
    @type parent: L{tables.SupItemGroup}
    """
    name = unicode(name)
    g = tables.SupItemGroup.by_parent_and_name(parent, name)
    if not g:
        g = tables.SupItemGroup(name=name, parent=parent)
        DBSession.add(g)
        DBSession.flush()
    return g

def add_supitemgroup_parent(child, parent):
    """
    Modifie le parent d'un groupe d'éléments supervisés.

    @param child: Groupe d'éléments supervisés fils.
    @type child: C{basestr} ou L{tables.SupItemGroup}
    @param parent: Groupe d'éléments supervisés parent.
    @type parent: C{basestr} ou L{tables.SupItemGroup} ou C{None}
    @deprecated: Cette méthode ne fonctionne correctement que lorsque
        les deux paramètres sont des instances de L{tables.SupItemGroup}.
        Dans le cas où l'un des paramètres est une chaîne de caractères,
        le premier groupe dont le nom correspond est utilisé. Il se peut
        que ce groupe ne soit pas celui voulu si vous posséder une
        arborescence dans laquelle le même nom de groupe peut apparaître
        sous plusieurs branches différentes.
    """
    if isinstance(child, basestring):
        child = tables.SupItemGroup.by_group_name(unicode(child))
    if isinstance(parent, basestring):
        parent = tables.SupItemGroup.by_group_name(unicode(parent))
    child.parent = parent
    DBSession.flush()

def add_supitemgrouppermission(group, usergroup, access='r'):
    """
    Associe une permission à un groupe d'utilisateurs sur un groupe
    d'objets.

    @param group: Groupe d'éléments supervisés sur lequel porte la permission.
    @type group: C{basestr} ou L{tables.SupItemGroup}
    @param usergroup: Groupe d'utilisateurs.
    @type usergroup: C{basestr} ou L{tables.UserGroup}
    @param access: Type d'accès donné. Les valeurs possibles sont
        'r' pour un accès en lecture seule et 'w' pour un accès en
        lecture/écriture.
    @return: Instance de la permission créée ou existante.
    @rtype: L{tables.DataPermission}
    @deprecated: L'exécution de cette fonction peut retourner un résultat
        inattendu lorsqu'une chaîne de caractères est utilisée pour spécifier
        le groupe d'éléments supervisés. Utilisez de préférence une instance
        de la classe L{tables.SupItemGroup} à la place.
    """
    if isinstance(group, basestring):
        group = tables.SupItemGroup.by_group_name(unicode(group))
    if isinstance(usergroup, basestring):
        usergroup = tables.UserGroup.by_group_name(unicode(usergroup))
    p = DBSession.query(tables.DataPermission).filter(
            tables.DataPermission.idgroup == group.idgroup
        ).filter(
            tables.DataPermission.idusergroup == usergroup.idgroup
        ).first()
    if not p:
        p = tables.DataPermission(
                group=group,
                usergroup=usergroup,
                access=unicode(access),
            )
        DBSession.add(p)
        DBSession.flush()
    return p

def add_host2group(host, group):
    """
    Ajoute un hôte à un groupe d'éléments supervisés.

    @param host: Hôte à ajouter au groupe.
    @type host: C{basestr} ou L{tables.Host}
    @param group: Groupe d'éléments supervisés auquel l'hôte
        doit être ajouté.
    @type group: C{basestr} ou L{tables.SupItemGroup}
    @deprecated: L'exécution de cette fonction peut retourner un résultat
        inattendu lorsqu'une chaîne de caractères est utilisée pour spécifier
        le groupe d'éléments supervisés. Utilisez de préférence une instance
        de la classe L{tables.SupItemGroup} à la place.
    """
    if isinstance(host, basestring):
        host = tables.Host.by_host_name(unicode(host))
    if isinstance(group, basestring):
        group = tables.SupItemGroup.by_group_name(unicode(group))
    if host not in group.supitems:
        group.supitems.append(host)
        DBSession.flush()

def add_lls2group(lls, group):
    """
    Ajoute une service de bas niveau à un groupe d'éléments supervisés.

    @param lls: Service de bas niveau à ajouter au groupe, sous la forme
        d'une instance ou d'un tuple (hôte, service).
    @type lls: C{tuple} ou L{tables.LowLevelService}
    @param group: Groupe auquel le service sera ajouté.
    @type group: C{basestr} ou L{tables.SupItemGroup}
    @deprecated: L'exécution de cette fonction peut retourner un résultat
    inattendu lorsqu'une chaîne de caractères est utilisée pour spécifier
    le groupe d'éléments supervisés. Utilisez de préférence une instance
    de la classe L{tables.SupItemGroup} à la place.
    """
    if isinstance(lls, basestring):
        raise ValueError("I need a host name too !")
    if isinstance(lls, tuple):
        lls = map(unicode, lls)
        lls = tables.LowLevelService.by_host_service_name(*lls)
    if isinstance(group, basestring):
        group = tables.SupItemGroup.by_group_name(unicode(group))
    if lls not in group.supitems:
        group.supitems.append(lls)
        DBSession.flush()


#
# Ventilation
#

def add_vigiloserver(name):
    """
    Ajoute un serveur de supervision Vigilo.

    @param name: Nom du service de supervision à ajouter.
    @type name: C{basestr}
    @return: Instance du serveur de supervision créée ou existante.
    @rtype: L{tables.VigiloServer}
    @note: Les serveurs de supervision sont gérés indépendamment
        des serveurs supervisés. Donc le serveur peut également
        apparaître dans la table L{table.Host}, mais ceci n'est
        pas obligatoire. Cette pratique est cependant recommandée.
    """
    name = unicode(name)
    s = tables.VigiloServer.by_vigiloserver_name(name)
    if not s:
        s = tables.VigiloServer(name=name)
        DBSession.add(s)
        DBSession.flush()
    return s

def add_application(name):
    """
    Ajoute une application liée à la supervision.

    @param name: Nom de l'application à ajouter.
    @type name: C{basestr}
    @return: Instance de l'application créée ou existante.
    @rtype: L{tables.Application}
    """
    name = unicode(name)
    a = tables.Application.by_app_name(name)
    if not a:
        a = tables.Application(name=name)
        DBSession.add(a)
        DBSession.flush()
    return a

def add_ventilation(host, server, application):
    """
    Ventile un hôte sur un serveur de supervision
    pour une application donnée.

    @param host: Hôte supervisé à ventiler.
    @type host: C{basestr} ou L{tables.Host}
    @param server: Serveur de supervision sur lequel ventiler.
    @type server: C{basestr} ou L{tables.VigiloServer}
    @param application: Application sur laquelle porte la ventilation.
    @type application: C{basestr} ou L{tables.Application}
    @return: Instance de ventilation créée.
        Cette fonction lèvera une exception si l'hôte est déjà ventilé
        sur un serveur de supervision pour l'application donnée.
    @rtype: L{tables.Ventilation}
    """
    if isinstance(host, basestring):
        host = tables.Host.by_host_name(unicode(host))
    if isinstance(server, basestring):
        server = tables.VigiloServer.by_vigiloserver_name(unicode(server))
    if isinstance(application, basestring):
        application = tables.Application.by_app_name(unicode(application))
    v = tables.Ventilation(
            idhost=host.idhost,
            idvigiloserver=server.idvigiloserver,
            idapp=application.idapp
        )
    DBSession.merge(v)
    DBSession.flush()
    return v


#
# États
#

def add_svc_state(service, statename, message):
    """
    Met à jour l'état d'un service de bas niveau.

    @param service: Service de bas niveau dont l'état doit être
        mis à jour, exprimé sous la forme d'une instance ou bien
        d'un tuple (hôte, service).
    @type service: C{tuple} ou L{tables.LowLevelService}
    @param statename: Nouvel état du service.
    @type statename: C{basestr}
    @param message: Message associé au nouvel état.
    @type message: C{basestr}
    """
    if isinstance(service, tuple):
        service = map(unicode, service)
        service = tables.LowLevelService.by_host_service_name(*service)
    elif isinstance(service, basestring):
        service = tables.HighLevelService.by_service_name(service)
    s = tables.State(idsupitem=service.idservice,
                    state=tables.StateName.statename_to_value(statename),
                    message=message)
    s = DBSession.merge(s)
    DBSession.flush()


#
# Cartographie
#

def add_map(name, group=None):
    """
    Ajoute une carte, en l'associant éventuellement à un groupe de cartes.

    @param name: Nom de la carte à ajouter.
    @type name: C{basestr}
    @param group: Groupe de cartes auquel la carte sera associée.
    @type group: C{basestr} ou L{tables.MapGroup} ou None
    @return: Instance de la carte créée ou existante.
    @rtype: L{tables.Map}
    @note: Si aucun L{group} n'est donné, la carte est automatiquement
        associée au groupe racine (Root) de la cartographie.
    @deprecated: L'exécution de cette fonction peut retourner un résultat
        inattendu lorsqu'une chaîne de caractères est utilisée pour spécifier
        le groupe de cartes. Utilisez de préférence une instance de la classe
        L{tables.MapGroup} à la place.
    """
    if group is None:
        # @TODO: le nom du groupe n'est peut-être pas unique.
        group = tables.MapGroup.by_group_name(u"Root")
    if isinstance(group, basestring):
        group = tables.MapGroup.by_group_name(unicode(group))
    name = unicode(name)
    m = tables.Map.by_group_and_title(group, name)
    if not m:
        m = tables.Map(
                mtime=datetime.today(),
                title=name,
                generated=True,
                background_color=u'',
                background_image=u'',
                background_position=u'',
                background_repeat=u'',
        )
        DBSession.add(m)
        m.groups.append(group)
        DBSession.flush()
    return m

def add_mapgroup(name, parent=None):
    """
    Ajoute un groupe de cartes.

    @param name: Nom du groupe à ajouter.
    @type name: C{basestr}
    @param parent: Instance du groupe parent de ce groupe.
    @type parent: L{tables.MapGroup}
    @return: Instance du groupe de cartes créée ou existante.
    @rtype: L{tables.MapGroup}
    """
    name = unicode(name)
    g = tables.MapGroup.by_parent_and_name(parent, name)
    if not g:
        g = tables.MapGroup(name=name, parent=parent)
        DBSession.add(g)
        DBSession.flush()
    return g

def add_map2group(map, group):
    """
    Ajoute une carte à un groupe de cartes.

    @param map: Carte à ajouter au groupe.
    @type map: L{tables.Map}
    @param group: Groupe de cartes auquel ajouter la carte.
    @type group: L{tables.MapGroup}
    """
    if map not in group.maps:
        group.maps.append(map)
        DBSession.flush()

def add_node_host(host, label, map, widget="ServiceElement",
                    x=None, y=None, icon=None, submaps=[]):
    if isinstance(host, basestring):
        host = tables.Host.by_host_name(unicode(host))
    n = tables.MapNodeHost.by_map_label(map, unicode(label))
    if not n:
        n = tables.MapNodeHost(label=unicode(label), idmap=map.idmap,
                              x_pos=x, y_pos=y, widget=unicode(widget),
                              idhost=host.idhost, icon=unicode(icon))
        DBSession.add(n)
    for submap in submaps:
        if submap.idmap not in [s.idmap for s in n.submaps]:
            n.submaps.append(submap)
    DBSession.flush()
    return n

def add_node_lls(lls, label, map, widget="ServiceElement",
                    x=None, y=None, icon=None, submaps=[]):
    if isinstance(lls, basestring):
        raise ValueError("I need a host name too !")
    if isinstance(lls, tuple):
        lls = [unicode(s) for s in lls]
        lls = tables.LowLevelService.by_host_service_name(*lls)
    n = tables.MapNodeLls.by_map_label(map, unicode(label))
    if not n:
        n = tables.MapNodeLls(label=unicode(label), idmap=map.idmap,
                              x_pos=x, y_pos=y, widget=unicode(widget),
                              idservice=lls.idservice, icon=unicode(icon))
        DBSession.add(n)
    for submap in submaps:
        if submap.idmap not in [s.idmap for s in n.submaps]:
            n.submaps.append(submap)
    DBSession.flush()
    return n

def add_node_hls(hls, label, map, widget="ServiceElement",
                    x=None, y=None, icon=None, submaps=[]):
    if isinstance(hls, basestring):
        hls = tables.HighLevelService.by_service_name(hls)
    n = tables.MapNodeHls.by_map_label(map, unicode(label))
    if not n:
        n = tables.MapNodeHls(label=unicode(label), idmap=map.idmap,
                              x_pos=x, y_pos=y, widget=unicode(widget),
                              idservice=hls.idservice, icon=unicode(icon))
        DBSession.add(n)
    for submap in submaps:
        if submap.idmap not in [s.idmap for s in n.submaps]:
            n.submaps.append(submap)
    DBSession.flush()
    return n

def add_mapsegment(from_node, to_node, map):
    if isinstance(from_node, basestring):
        from_node = tables.MapNode.by_map_label(map, unicode(from_node))
    if isinstance(to_node, basestring):
        to_node = tables.MapNode.by_map_label(map, unicode(to_node))
    ms = tables.MapSegment(idfrom_node=from_node.idmapnode,
                           idto_node=to_node.idmapnode,
                           idmap=map.idmap)
    DBSession.merge(ms)
    DBSession.flush()
    return ms

def add_mapllslink(from_node, to_node, lls, map):
    if isinstance(from_node, basestring):
        from_node = tables.MapNode.by_map_label(map, unicode(from_node))
    if isinstance(to_node, basestring):
        to_node = tables.MapNode.by_map_label(map, unicode(to_node))
    if isinstance(lls, tuple):
        lls = [unicode(s) for s in lls]
        lls = tables.LowLevelService.by_host_service_name(*lls)
    pds_in = add_perfdatasource('ineth0', lls.host)
    pds_out = add_perfdatasource('outeth0', lls.host)
    ms = tables.MapLlsLink(idfrom_node=from_node.idmapnode,
                               idto_node=to_node.idmapnode,
                               idref=lls.idservice, idmap=map.idmap,
                               ds_from_to_to=pds_out,
                               ds_to_to_from=pds_in)
    DBSession.merge(ms)
    DBSession.flush()
    return ms


#
# Métrologie
#

def add_perfdatasource(name, host, label=None, max=None,
    vigiloserver="localhost"):
    name = unicode(name)
    if isinstance(host, basestring):
        host = tables.Host.by_host_name(unicode(host))
    ds = tables.PerfDataSource.by_host_and_source_name(host, name)
    if not ds:
        if label:
            label = unicode(label)
        ds = tables.PerfDataSource(name=name,
                                   type=u"GAUGE",
                                   host=host,
                                   label=label,
                                   max=max,
                                   )
        DBSession.add(ds)
        add_ventilation(host, vigiloserver, 'vigirrd')
        DBSession.flush()
    return ds

def add_graph(name, vlabel="", template="graph"):
    name = unicode(name)
    gr = tables.Graph(name=name,
                      vlabel=unicode(vlabel),
                      template=unicode(template),
                      )
    DBSession.add(gr)
    DBSession.flush()
    return gr

def add_perfdatasource2graph(ds, graph):
    if isinstance(graph, int):
        graph = DBSession.query(tables.Graph).get(graph)
    if isinstance(ds, tuple):
        ds = tables.PerfDataSource.by_host_and_source_name(*ds)
    if ds not in graph.perfdatasources:
        graph.perfdatasources.append(ds)
        DBSession.flush()

def add_graphgroup(name, parent=None):
    name = unicode(name)
    g = tables.GraphGroup.by_parent_and_name(parent, name)
    if not g:
        g = tables.GraphGroup(name=name, parent=parent)
        DBSession.add(g)
        DBSession.flush()
    return g

def add_graph2group(graph, group):
    if isinstance(group, basestring):
        group = tables.GraphGroup.by_group_name(unicode(group))
    if isinstance(graph, int):
        graph = DBSession.query(tables.Graph).get(graph)
    if graph not in group.graphs:
        group.graphs.append(graph)
        DBSession.flush()

# Affectation des permissions aux groupes de cartes.
def add_MapGroupPermission(group, usergroup, access='w'):
    if isinstance(usergroup, basestring):
        usergroup = tables.UserGroup.by_group_name(unicode(usergroup))
    p = DBSession.query(tables.DataPermission).filter(
            tables.DataPermission.idgroup == group.idgroup
        ).filter(
            tables.DataPermission.idusergroup == usergroup.idgroup
        ).first()
    if not p:
        p = tables.DataPermission(
                group=group,
                usergroup=usergroup,
                access=unicode(access),
            )
        DBSession.add(p)
        DBSession.flush()
    return p

# Ajout de user et et son groupe associé.
def add_user(username, email, fullname, password, groupname):
    """
    Ajoute un utilisateur, en l'associant éventuellement
    à un groupe d'utilisateurs.

    @param username: Nom de l'utilisateur.
    @type username: C{basestr}
    @param email: Adresse email de l'utilisateur.
    @type email: C{unicode} ou C{None}
    @param fullname: Nom complet de l'utilisateur.
    @type fullname: C{unicode}
    @param password: Mot de passe de l'utilisateur.
    @type password: C{unicode}
    @param groupname: Nom du groupe d'utilisateurs
        auquel associer le nouvel utilisateur.
    @type groupname: C{basestr}
    """
    name = unicode(username)
    user = tables.User.by_user_name(name)
    if not user:
        user = tables.User(user_name=name,
                           email=email,
                           fullname=fullname,
                           password=password)
        DBSession.add(user)
        DBSession.flush()
    else:
        raise ValueError, "User already exists"

    groupname = unicode(groupname)
    group = tables.UserGroup.by_group_name(groupname)
    if not group:
        group = tables.UserGroup(group_name=groupname)
        DBSession.add(group)
        DBSession.flush()

    if not user in group.users:
        group.users.append(user)
        DBSession.add(group)
    DBSession.flush()

def add_usergroup(groupname):
    """
    Ajoute un groupe d'utilisateurs.

    @param groupname: Nom du groupe.
    @type groupname: C{basestr}
    @return: Instance du groupe d'utilisateurs créée ou existante.
    @rtype: L{tables.UserGroup}
    """
    groupname = unicode(groupname)
    group = tables.UserGroup.by_group_name(groupname)
    if not group:
        group = tables.UserGroup(group_name=groupname)
        DBSession.add(group)
        DBSession.flush()
    return group

# Ajout d'une permission dans un groupe de users
def add_usergroup_permission(group, perm):
    """
    Associe une permission à un groupe d'utilisateurs.

    @param group: Groupe d'utilisateurs qui recevra la permission.
    @type group: C{basestr} ou L{tables.UserGroup}
    @param perm: Permission à accorder au groupe d'utilisateurs.
    @type perm: C{basestr} ou L{tables.Permission}
    """
    if isinstance(group, basestring):
        group = tables.UserGroup.by_group_name(unicode(group))
    if isinstance(perm, basestring):
        perm = tables.Permission.by_permission_name(unicode(perm))
    if not perm:
        return
    perm.usergroups.append(group)
    DBSession.add(perm)
    DBSession.flush()
