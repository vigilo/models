# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Host"""
from __future__ import absolute_import

from sqlalchemy import Column
from sqlalchemy.types import Integer, Unicode, UnicodeText
from sqlalchemy.orm import relation

from vigilo.models.session import DBSession, ForeignKey
from vigilo.models.tables.secondary_tables import HOST_HOSTCLASS_TABLE, \
                                                    HOST_GROUP_TABLE
from vigilo.models.tables.supitem import SupItem

__all__ = ('Host', )

class Host(SupItem):
    """
    Informations sur un hôte du parc informatique.
    
    @ivar idhost: Identifiant de l'hôte.
    @ivar name: Nom complet (FQDN) unique de l'hôte.
    @ivar checkhostcmd: Commande à exécuter pour vérifier l'état de l'hôte.
    @ivar description: Une description intelligible de l'hôte.
    @ivar hosttpl: ???.
    @todo: documenter l'attribut hosttpl.
    @ivar mainip: Adresse IP (v4 ou v6) principale de cet hôte.
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
    __mapper_args__ = {'polymorphic_identity': u'host'}

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

    mainip = Column(
        Unicode(40),    # 39 caractères sont requis pour stocker une IPv6
                        # sous forme canonique. On arrondit à 40 caractères.
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

    groups = relation('HostGroup', secondary=HOST_GROUP_TABLE,
                back_populates='hosts', lazy=True)

    hostclasses = relation('HostClass', secondary=HOST_HOSTCLASS_TABLE,
        back_populates='hosts', lazy=True)

    services = relation('LowLevelService', lazy=True,
        primaryjoin='Host.idhost == LowLevelService.idhost')

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
    
    def get_key(self):
        """ Clé utile pour implémenter la détection de changement.
        """
        return "h:%s" % self.name

