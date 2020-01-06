# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2020 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèle pour la table Host"""
from __future__ import absolute_import

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.orm import relation
from sqlalchemy.orm import EXT_CONTINUE

from vigilo.models.session import DBSession
from vigilo.models.tables.secondary_tables import HOST_HOSTCLASS_TABLE
from vigilo.models.tables.supitem import SupItem, SupItemMapperExt
from vigilo.models.tables.conffile import ConfFile

__all__ = ('Host', )


class HostMapperExt(SupItemMapperExt):
    """
    Force la propagation de la suppression d'un hôte à toutes ses
    représentations cartographiques (MapNodeHost).

    Sans cela, la suppression du MapNodeHost est bien faite par PGSQL grâce au
    "ON DELETE CASCADE", mais l'instance parente (MapNode) est laissée en
    place.

    Pour les détails, voir le ticket #57.
    """
    def before_delete(self, mapper, connection, instance):
        """
        On utilise before_delete() plutôt qu' after_delete() parce qu'avec
        after_delete() le ON DELETE CASCADE s'est déjà produit et on a plus de
        MapNodeHost correspondant en base.
        """
        from vigilo.models.tables.mapnode import MapNodeHost
        mapnodes = DBSession.query(MapNodeHost).filter(
                MapNodeHost.idhost == instance.idhost
            ).all()
        for mapnode in mapnodes:
            DBSession.delete(mapnode)
        return EXT_CONTINUE


class Host(SupItem):
    """
    Informations sur un hôte du parc informatique.

    @ivar idhost: Identifiant de l'hôte.
    @ivar name: Nom complet (FQDN) unique de l'hôte.
    @ivar description: Une description intelligible de l'hôte.
    @ivar hosttpl: ???.
    @todo: documenter l'attribut hosttpl.
    @ivar address: Adresse permettant de communiquer avec cet hôte.
        Il peut s'agir d'une adresse IP (v4 ou v6) ou d'un FQDN.
    @ivar snmpcommunity: Nom de la communauté SNMP auquel l'hôte appartient.
    @ivar snmpport: Port à utiliser pour le protocole SNMP.
    @ivar snmpoidsperpdu: Nombre d'OIDs à transmettre par PDU.
    @ivar snmpversion: Version du protocole SNMP à utiliser.
    @ivar groups: Liste des groupes d'hôtes auxquels cet hôte appartient.
    @ivar hostclasses: Classes d'hôtes attachées à l'hôte.
    @ivar services: Liste des services de bas niveau configurés sur cet hôte.
    """
    __tablename__ = 'vigilo_host'
    __mapper_args__ = {
        'polymorphic_identity': 1,
        'extension': HostMapperExt(),
    }

    idhost = Column(
        Integer,
        ForeignKey(
            SupItem.idsupitem,
            onupdate='CASCADE',
            ondelete='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
        autoincrement=False,
    )

    idconffile = Column(
        Integer,
        ForeignKey(
            ConfFile.idconffile,
            onupdate='CASCADE',
            ondelete='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        nullable=True
    )

    name = Column(
        Unicode(255),
        index=True, unique=True, nullable=False)

    description = Column(Unicode(512), nullable=True)

    hosttpl = Column(
        Unicode(255),
        nullable=False)

    address = Column(
        Unicode(255),   # Longueur maximale d'un FQDN selon la RFC 2181.
        nullable=False)

    snmpcommunity = Column(
        Unicode(255),
        nullable=False)

    snmpport = Column(Integer, nullable=False)

    snmpoidsperpdu = Column(Integer)

    snmpversion = Column(Unicode(255))

    conffile = relation('ConfFile', back_populates="hosts", lazy=True)

    hostclasses = relation('HostClass', secondary=HOST_HOSTCLASS_TABLE,
        back_populates='hosts', lazy=True)

    services = relation('LowLevelService', lazy=True, cascade="all",
        primaryjoin='Host.idhost == LowLevelService.idhost')

    perfdatasources = relation('PerfDataSource', lazy=True, cascade="all",
                        back_populates='host')

    def _get_graphs(self):
        from vigilo.models.tables.graph import Graph
        from vigilo.models.tables.perfdatasource import PerfDataSource
        from vigilo.models.tables.secondary_tables import \
            GRAPH_PERFDATASOURCE_TABLE
        return DBSession.query(Graph).distinct().join(
                        (GRAPH_PERFDATASOURCE_TABLE, \
                            GRAPH_PERFDATASOURCE_TABLE.c.idgraph == \
                            Graph.idgraph),
                        (PerfDataSource, PerfDataSource.idperfdatasource == \
                            GRAPH_PERFDATASOURCE_TABLE.c.idperfdatasource),
                    ).filter(PerfDataSource.idhost == self.idhost
                    ).all()
    graphs = property(_get_graphs)


    def __init__(self, **kwargs):
        """Initialise un hôte."""
        super(Host, self).__init__(**kwargs)

    def __unicode__(self):
        """
        Formatte un C{Host} pour l'afficher dans les formulaires.

        Le nom de l'hôte est utilisé pour le représenter dans les formulaires.

        @return: Le nom de l'hôte.
        @rtype: C{str}
        """
        return self.name

    def __repr__(self):
        try:
            return str(self.name)
        except Exception: # pylint: disable-msg=W0703
            # W0703: Catch "Exception"
            return super(Host, self).__str__()

    @classmethod
    def by_host_name(cls, hostname):
        """
        Renvoie l'hôte dont le nom est L{hostname}.

        @param hostname: Nom de l'hôte voulu.
        @type hostname: C{unicode}
        @return: L'hôte demandé.
        @rtype: L{Host}
        """
        return DBSession.query(cls).filter(cls.name == hostname).first()
