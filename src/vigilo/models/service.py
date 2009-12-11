# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Service"""
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import UnicodeText, Unicode, Integer
from sqlalchemy.orm import synonym, relation
from sqlalchemy.schema import UniqueConstraint

from vigilo.models.vigilo_bdd_config import bdd_basename, DeclarativeBase
from vigilo.models.session import DBSession
from vigilo.models.secondary_tables import SERVICE_GROUP_TABLE
from vigilo.models.supitem import SupItem
from vigilo.models.host import Host

__all__ = ('Service', )

class Service(SupItem):
    """
    Service générique.

    @ivar name: Nom du service.
    @ivar op_dep: Le type d'opération à appliquer aux dépendances de ce
        service de haut niveau ('+', '&' ou '|').
    @ivar servicegroups: Liste des groupes de services auxquels
        ce service appartient.
    @ivar tags: Liste des libellés associés à ce service.
    @ivar dependancies: Liste des services dont ce service dépend.
        Pour les services techniques, cette liste est toujours vide.
    """
    __tablename__ = bdd_basename + 'service'

    idservice = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'supitem.idsupitem',
            onupdate='CASCADE', ondelete='CASCADE',
        ),
        primary_key=True, autoincrement=False,
    )

    servicename = Column(
        Unicode(255),
        index=True, nullable=False,
    )

    op_dep = Column(
        Unicode(1),
        nullable=False,
    )

    @property
    def dependancies(self):
        """
        Renvoie la liste des dépendances de ce service.

        Pour un L{Service} technique (de bas niveau), il n'y a jamais de
        dépendances, donc cette méthode renvoie une liste vide.
        Cette méthode existe afin de permettre d'appeler C{obj.dependancies}
        sur un service quelconque (de bas ou de haut niveau) sans provoquer
        d'erreurs.
        """
        return []


    def __init__(self, **kwargs):
        """Initialise un service."""
        super(Service, self).__init__(**kwargs)

    def __unicode__(self):
        """
        Formatte un C{Service} pour l'afficher dans les formulaires.

        Le nom du service est utilisé pour le représenter dans les formulaires.

        @return: Le nom du service.
        @rtype: C{str}
        """
        return self.servicename


class ServiceLowLevel(Service):
    """
    Service de bas niveau (service technique).

    @ivar command: Commande à exécuter pour vérifier l'état du service.
    """
    __tablename__ = bdd_basename + 'servicelowlevel'
    __table_args__ = (
        UniqueConstraint('idservice', 'idhost'),
        {}
    )
    __mapper_args__ = {'polymorphic_identity': u'lowlevel'}

    idservice = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'service.idservice',
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        autoincrement=False, primary_key=True,
    )

    idhost = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'host.idhost',
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        nullable=False,
    )

    host = relation('Host', foreign_keys=[idhost],
        primaryjoin='ServiceLowLevel.idhost == Host.idsupitem')

    command = Column(
        UnicodeText,
        default=u'', nullable=False,
    )

    weight = Column(
        Integer,
        nullable=False,
    )

    __priority = Column(
        'priority', Integer,
        nullable=False,
    )

    def _get_priority(self):
        """Renvoie la priorité associée à un couple hôte/service."""
        return self.__priority

    # XXX on devrait s'assurer que la priorité est bornée.
    # Ceci permettra aussi de définir les limites pour Rum (Vigicore).
    def _set_priority(self, priority):
        """Modifie la priorité associée à un couple hôte/service."""
        self.__priority = priority

    priority = synonym(__priority,
        descriptor=property(_get_priority, _set_priority))

    groups = relation('ServiceGroup', secondary=SERVICE_GROUP_TABLE,
                back_populates='services')

    def __init__(self, **kwargs):
        super(ServiceLowLevel, self).__init__(**kwargs)

    @classmethod
    def by_host_service_name(cls, hostname, servicename):
        """
        Renvoie le service de bas niveau dont le nom d'hôte
        est L{hostname} et le nom de service est L{servicename}.
        
        @param hostname: Nom de l'hôte auquel est rattaché le service.
        @type hostname: C{unicode}
        @param servicename: Nom du service voulu.
        @type servicename: C{unicode}
        @return: Le service de bas niveau demandé.
        @rtype: L{ServiceLowLevel} ou None
        """
        return DBSession.query(cls).join(
                (Host, Host.idsupitem == cls.idhost)
            ).filter(Host.name == hostname
            ).filter(cls.servicename == servicename
            ).first()


class ServiceHighLevel(Service):
    """
    Service de haut niveau.

    @ivar message: Message à afficher dans Vigiboard lorsque le service
        passe dans un état autre que OK.
    @ivar warning_threshold: Seuil à partir duquel le service passe de
        l'état OK à l'état WARNING.
    @ivar critical_threshold: Seuil à partir duquel le service passe de
        l'état WARNING à l'état CRITICAL.
    """
    __tablename__ = bdd_basename + 'servicehighlevel'
    __mapper_args__ = {'polymorphic_identity': u'highlevel'}

    idservice = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'service.idservice',
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        autoincrement=False, primary_key=True,
    )

    message = Column(
        UnicodeText,
        nullable=False,
    )

    warning_threshold = Column(
        Integer,
        nullable=False,
    )

    critical_threshold = Column(
        Integer,
        nullable=False,
    )

    weight = Column(
        Integer,
        nullable=True,
    )

    impacts = relation('ImpactedHLS', back_populates='hls', lazy='dynamic')

    def __init__(self, **kwargs):
        super(ServiceHighLevel, self).__init__(**kwargs)

    @classmethod
    def by_service_name(cls, servicename):
        """
        Renvoie le service de haut niveau dont le nom est L{servicename}.
        
        @param servicename: Nom du service de haut niveau voulu.
        @type servicename: C{unicode}
        @return: Le service de haut niveau demandé.
        @rtype: L{ServiceHighLevel} ou None
        """
        return DBSession.query(cls).filter(
            cls.servicename == servicename).first()

