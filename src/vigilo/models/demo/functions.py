# -*- coding: utf-8 -*-

import os
from datetime import datetime

from sqlalchemy import and_

from vigilo.models.session import DBSession
from vigilo.models import tables


#
# Base
#

def add_host(hostname):
    h = tables.Host.by_host_name(unicode(hostname))
    if not h:
        h = tables.Host(
                name=unicode(hostname),
                checkhostcmd=u'dummy',
                hosttpl=u'dummy',
                mainip=u"127.0.0.1",
                snmpcommunity=u"public",
                snmpport=161,
                weight=0)
        DBSession.add(h)
        DBSession.flush()
    return h

def add_lowlevelservice(host, servicename, statename="OK", message="", weight=100):
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
                command=u"dummy",
                op_dep=u"")
        DBSession.add(s)
        DBSession.flush()
    return s

def add_highlevelservice(servicename, op_dep="", message="", priority=1):
    servicename = unicode(servicename)
    s = tables.HighLevelService.by_service_name(servicename)
    if not s:
        s = tables.HighLevelService(
                servicename=servicename,
                priority=priority,
                weight=0,
                message=unicode(message),
                warning_threshold=300,
                critical_threshold=150,
                op_dep=unicode(op_dep))
        DBSession.add(s)
        DBSession.flush()
    return s

def add_dependency(dependent, depended):
    host, service = dependent
    if host is None:        # HLS
        supitem1 = tables.HighLevelService.by_service_name(unicode(service))
    elif service is None:   # Host
        supitem1 = tables.Host.by_host_name(unicode(host))
    else:                   # LLS
        supitem1 = tables.LowLevelService.by_host_service_name(
                        unicode(host), unicode(service))

    host, service = depended
    if host is None:        # HLS
        supitem2 = tables.HighLevelService.by_service_name(unicode(service))
    elif service is None:   # Host
        supitem2 = tables.Host.by_host_name(unicode(host))
    else:                   # LLS
        supitem2 = tables.LowLevelService.by_host_service_name(
                        unicode(host), unicode(service))

    tables.Dependency.get_or_create(supitem1, supitem2)
    DBSession.flush()


#
# Groupes
#

def add_supitemgroup(name, parent=None):
    g = DBSession.query(tables.SupItemGroup).filter(
            tables.SupItemGroup.name == unicode(name)
        ).first()
    if not g:
        if parent:
            g = tables.SupItemGroup(name=unicode(name),
                                 idparent=parent.idgroup)
        else:
            g = tables.SupItemGroup(name=unicode(name))
        DBSession.add(g)
        DBSession.add(tables.grouphierarchy.GroupHierarchy(
                      parent=g, child=g, hops=0))
        g.permissions.append(tables.Permission.by_permission_name(u"manage"))
        DBSession.flush()
    return g

def add_supitemgroup_parent(child, parent):
    if isinstance(child, basestring):
        child = tables.SupItemGroup.by_group_name(unicode(child))
    if isinstance(parent, basestring):
        parent = tables.SupItemGroup.by_group_name(unicode(parent))
    tables.grouphierarchy.GroupHierarchy.get_or_create(
                        parent=parent, child=child, hops=1)
    DBSession.flush()

def add_supitemgrouppermission(group, perm):
    if isinstance(group, basestring):
        group = tables.SupItemGroup.by_group_name(unicode(group))
    if isinstance(perm, basestring):
        perm = tables.Permission.by_permission_name(unicode(perm))
    if perm not in group.permissions:
        group.permissions.append(perm)
        DBSession.flush()

def add_host2group(host, group):
    if isinstance(host, basestring):
        host = tables.Host.by_host_name(unicode(host))
    if isinstance(group, basestring):
        group = tables.SupItemGroup.by_group_name(unicode(group))
    if host not in group.supitems:
        group.supitems.append(host)
        DBSession.flush()

def add_lls2group(lls, group):
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
    name = unicode(name)
    s = tables.VigiloServer.by_vigiloserver_name(name)
    if not s:
        s = tables.VigiloServer(name=name)
        DBSession.add(s)
        DBSession.flush()
    return s

def add_application(name):
    name = unicode(name)
    a = tables.Application.by_app_name(name)
    if not a:
        a = tables.Application(name=name)
        DBSession.add(a)
        DBSession.flush()
    return a

def add_ventilation(host, server, application):
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
    s = DBSession.query(tables.State).filter(
                tables.State.idsupitem == service.idservice
            ).first()
    if not s:
        s = tables.State(idsupitem=service.idservice,
                        state=tables.StateName.statename_to_value(statename),
                        message=message)
        s = DBSession.merge(s)
        DBSession.flush()


#
# Cartographie
#

def add_map(name):
    m = DBSession.query(tables.Map).filter(
            tables.Map.title == unicode(name)
        ).first()
    if not m:
        m = tables.Map(
                mtime=datetime.today(),
                title=unicode(name),
                generated=True,
                background_color=u'',
                background_image=u'France',
                background_position=u'top right',
                background_repeat=u'no-repeat',
        )
        DBSession.add(m)
    return m


def add_node_hls(hls, label, map, submaps, widget="ServiceElement"):
    n = DBSession.query(tables.MapNodeHls).join(
            (tables.HighLevelService,
             tables.HighLevelService.idservice == tables.MapNodeHls.idservice)
        ).filter(
            and_(
                tables.MapNodeHls.idservice == hls.idservice,
                tables.MapNodeHls.idmap == map.idmap
            )).first()
    if n:
        n = DBSession.merge(n)
    else:
        n = tables.MapNodeHls(label=unicode(label), idmap=map.idmap,
                              x_pos=None, y_pos=None, widget=unicode(widget),
                              idservice=hls.idservice, serviceicon=None)
        DBSession.add(n)
    for submap in submaps:
        if submap.idmap not in [s.idmap for s in n.submaps]:
            n.submaps.append(submap)
    DBSession.flush()
    return n


#
# Métrologie
#

def add_perfdatasource(name, lls, label=None, max=None):
    name = unicode(name)
    if isinstance(lls, basestring):
        raise ValueError("I need a host name too !")
    elif isinstance(lls, tuple):
        lls = map(unicode, lls)
        lls = tables.LowLevelService.by_host_service_name(*lls)
    ds = tables.PerfDataSource.by_service_and_source_name(lls, name)
    if not ds:
        if label:
            label = unicode(label)
        ds = tables.PerfDataSource(name=name,
                                   type=u"GAUGE",
                                   idservice=lls.idservice,
                                   label=label,
                                   max=max,
                                   )
        DBSession.add(ds)
        DBSession.flush()
    return ds

def add_graph(name, vlabel="", template="graph"):
    name = unicode(name)
    gr = tables.Graph.by_graph_name(name)
    if not gr:
        gr = tables.Graph(name=name,
                          vlabel=unicode(vlabel),
                          template=unicode(template),
                          )
        DBSession.add(gr)
        DBSession.flush()
    return gr

def add_perfdatasource2graph(ds, graph):
    if isinstance(graph, basestring):
        graph = tables.Graph.by_graph_name(unicode(graph))
    if isinstance(ds, tuple):
        ds = tables.PerfDataSource.by_service_and_source_name(*ds)
    if ds not in graph.perfdatasources:
        graph.perfdatasources.append(ds)
        DBSession.flush()

def add_graphgroup(name):
    name = unicode(name)
    g = tables.GraphGroup.by_group_name(name)
    if not g:
        g = tables.GraphGroup(name=name)
        DBSession.add(g)
        DBSession.flush()
    return g

def add_graph2graphgroup(graph, group):
    if isinstance(group, basestring):
        group = tables.GraphGroup.by_group_name(unicode(group))
    if isinstance(graph, basestring):
        graph = tables.Graph.by_graph_name(unicode(graph))
    if graph not in group.graphs:
        group.graphs.append(graph)
        DBSession.flush()

