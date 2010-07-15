# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Host"""
from __future__ import absolute_import

from sqlalchemy import Column
from sqlalchemy.types import Integer, Unicode, UnicodeText
from sqlalchemy.orm import relation
from sqlalchemy.orm import EXT_CONTINUE

from vigilo.models.session import DBSession, ForeignKey
from vigilo.models.tables.secondary_tables import HOST_HOSTCLASS_TABLE
from vigilo.models.tables.supitem import SupItem, SupItemMapperExt

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
    @ivar checkhostcmd: Commande à exécuter pour vérifier l'état de l'hôte.
    @ivar description: Une description intelligible de l'hôte.
    @ivar hosttpl: ???.
    @todo: documenter l'attribut hosttpl.
    @ivar address: Adresse permettant de communiquer avec cet hôte.
        Il peut s'agir d'une adresse IP (v4 ou v6) ou d'un FQDN.
    @ivar snmpcommunity: Nom de la communauté SNMP auquel l'hôte appartient.
    @ivar snmpport: Port à utiliser pour le protocole SNMP.
    @ivar snmpoidsperpdu: Nombre d'OIDs à transmettre par PDU.
    @ivar snmpversion: Version du protocole SNMP à utiliser.
    @ivar weight: Poids affecté à cet hôte pour le calcul de l'état
        des services de haut niveau qui en dépendent.
    @ivar groups: Liste des groupes d'hôtes auxquels cet hôte appartient.
    @ivar hostclasses: Classes d'hôtes attachées à l'hôte.
    @ivar services: Liste des services de bas niveau configurés sur cet hôte.
    """
    __tablename__ = 'host'
    __mapper_args__ = {
        'polymorphic_identity': u'host',
        'extension': HostMapperExt(),
    }

    idhost = Column(
        Integer,
        ForeignKey(
            SupItem.idsupitem,
            onupdate='CASCADE', ondelete='CASCADE',
        ),
        primary_key=True, autoincrement=False,
    )

    name = Column(
        Unicode(255),
        index=True, unique=True, nullable=False)

    checkhostcmd = Column(
        UnicodeText,
        nullable=False)

    description = Column(
        UnicodeText,
        nullable=True)

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

    weight = Column(
        Integer,
        nullable=False,
    )

    hostclasses = relation('HostClass', secondary=HOST_HOSTCLASS_TABLE,
        back_populates='hosts', lazy=True)

    services = relation('LowLevelService', lazy=True, cascade="all",
        primaryjoin='Host.idhost == LowLevelService.idhost')

    perfdatasources = relation('PerfDataSource', lazy=True, cascade="all",
                        back_populates='host')


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
        except Exception:
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

