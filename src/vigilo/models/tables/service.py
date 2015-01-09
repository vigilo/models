# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2015 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèle pour la table Service"""
from sqlalchemy import Column
from sqlalchemy.types import UnicodeText, Unicode, Integer
from sqlalchemy.orm import relation, EXT_CONTINUE
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.associationproxy import association_proxy

from vigilo.models.session import DBSession, ForeignKey
from vigilo.models.tables.supitem import SupItem, SupItemMapperExt
from vigilo.models.tables.host import Host
from vigilo.models.tables.hlspriority import HLSPriority

__all__ = ('Service', 'LowLevelService', 'HighLevelService')


class LlsMapperExt(SupItemMapperExt):
    """
    Force la propagation de la suppression d'un service à toutes ses
    représentations cartographiques (MapNodeService).

    Sans cela, la suppression du MapNodeService est bien faite par PGSQL grâce
    au "ON DELETE CASCADE", mais l'instance parente (MapNode) est laissée en
    place.

    Pour les détails, voir le ticket #57.

    @TODO: à factoriser entre les services, voire avec les hôtes et les
        supitems
    """
    def before_delete(self, mapper, connection, instance):
        """
        On utilise before_delete() plutôt qu' after_delete() parce qu'avec
        after_delete() le ON DELETE CASCADE s'est déjà produit et on a plus de
        MapNodeService correspondant en base.
        """
        from vigilo.models.tables.mapnode import MapNodeLls
        mapnodes = DBSession.query(MapNodeLls).filter(
                MapNodeLls.idservice == instance.idservice
            ).all()
        for mapnode in mapnodes:
            DBSession.delete(mapnode)
        return EXT_CONTINUE

class HlsMapperExt(SupItemMapperExt):
    """
    Force la propagation de la suppression d'un service à toutes ses
    représentations cartographiques (MapNodeService).

    Sans cela, la suppression du MapNodeService est bien faite par PGSQL grâce
    au "ON DELETE CASCADE", mais l'instance parente (MapNode) est laissée en
    place.

    Pour les détails, voir le ticket #57.

    @TODO: à factoriser entre les services, voire avec les hôtes et les
        supitems
    """
    def before_delete(self, mapper, connection, instance):
        """
        On utilise before_delete() plutôt qu' after_delete() parce qu'avec
        after_delete() le ON DELETE CASCADE s'est déjà produit et on a plus de
        MapNodeService correspondant en base.
        """
        from vigilo.models.tables.mapnode import MapNodeHls
        mapnodes = DBSession.query(MapNodeHls).filter(
                MapNodeHls.idservice == instance.idservice
            ).all()
        for mapnode in mapnodes:
            DBSession.delete(mapnode)
        return EXT_CONTINUE


class Service(SupItem):
    """
    Service générique.
    """
    # Pour la compatibilité avec les versions précédentes du modèle.
    idservice = SupItem.idsupitem

    # Nécessaire pour pouvoir récupérer uniquement
    # des instances de services et pas d'hôtes.
    __mapper_args__ = {
        'polymorphic_identity': 2,
    }

class LowLevelService(Service):
    """
    Service de bas niveau (service technique).

    @ivar idservice: Identifiant du service.
    @ivar servicename: Nom du service.
    @ivar idhost: Identifiant de l'L{Host} sur lequel ce service est configuré.
    @ivar host: Instande de l'L{Host} sur lequel ce service est configuré.
    @ivar command: Commande à exécuter pour vérifier l'état du service.
    @ivar idcollector: Identifiant du Collector pour ce service.
    @ivar collector: Collector pour ce service.
    """
    __tablename__ = 'lowlevelservice'
    __table_args__ = (
        UniqueConstraint('servicename', 'idhost'),
        {}
    )

    idservice = Column(
        Integer,
        ForeignKey(
            SupItem.idsupitem,
            ondelete='CASCADE',
            onupdate='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        autoincrement=False,
        primary_key=True,
    )

    servicename = Column(
        Unicode(255),
        index=True, nullable=False,
    )

    idhost = Column(
        Integer,
        ForeignKey(
            Host.idhost,
            ondelete='CASCADE',
            onupdate='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        nullable=False,
    )

    host = relation('Host', foreign_keys=[idhost],
        primaryjoin='LowLevelService.idhost == Host.idsupitem')

    command = Column(
        Unicode(512),
        default=u'',
        nullable=False,
    )

    # On fait référence à SupItem plutôt qu'à LowLevelService,
    # même si on sait que le collecteur est un service de bas niveau,
    # afin de contourner un bug de SQLAlchemy avec les relations
    # auto-référentielles et l'héritage.
    idcollector = Column(
        Integer,
        ForeignKey(
            SupItem.idsupitem,
            ondelete='SET NULL',
            onupdate='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        default=None,
        nullable=True,
    )

    collector = relation('Service', foreign_keys=[idcollector],
        primaryjoin='LowLevelService.idcollector == Service.idsupitem',
        lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 3,
        'extension': LlsMapperExt(),
        'inherit_condition': idservice == SupItem.idsupitem,
    }

    def __init__(self, **kwargs):
        """Initialisation de l'objet."""
        super(LowLevelService, self).__init__(**kwargs)

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
        @rtype: L{LowLevelService} ou None
        """
        return DBSession.query(cls).join(
                (Host, Host.idsupitem == cls.idhost)
            ).filter(Host.name == hostname
            ).filter(cls.servicename == servicename
            ).first()

    def __unicode__(self):
        """Représentation unicode de l'objet."""
        return u"%s (%s)" % (self.servicename, self.host.name)

    def __repr__(self):
        # Le service n'a pas encore de nom (on est en train de le créer).
        if not self.servicename:
            return super(LowLevelService, self).__repr__()
        # Le service n'a pas encore d'hôte où l'hôte n'a pas encore de nom
        # (il est en cours de création).
        if not (self.host and self.host.name):
            return '<%s "%s" on ?>' % (
                self.__class__.__name__,
                self.servicename.encode('utf-8')
            )
        return "<%s \"%s\" on \"%s\">" % (
            self.__class__.__name__,
            self.servicename.encode('utf-8'),
            self.host.name.encode('utf-8')
        )

    def is_allowed_for(self, user, perm_type="r"):
        """
        Vérifie que l'utilisateur fourni en paramètre à le droit d'accéder
        au service, avec la permission optionnellement spécifiée.
        L'accès au service est accordé si l'utilisateur appartient à un
        groupe qui a explicitement la permission sur ce service, ou bien
        si l'utilisateur a la permission d'accéder à l'hôte qui héberge
        ce service.

        @todo: probablement à optimiser, ça fait beaucoup de requêtes.
        @todo: pour le moment, le paramètre perm_type n'est pas utilisé.

        @param user: L'utilisateur dont la permission est à tester
        @type  user: L{User}
        @param perm_type: Type d'accès, par défaut "r"
        @type  perm_type: C{str}
        @return: True si l'accès est autorisé, False sinon.
        @rtype: C{bool}
        """
        # On regarde si l'utilisateur a une permission explicite
        # sur le service (en fait, sur le supitem directement).
        if super(LowLevelService, self).is_allowed_for(user, perm_type):
            return True

        # Accès indirect (l'utilisateur a les permissions sur l'hôte).
        return self.host.is_allowed_for(user, perm_type)


class HighLevelService(Service):
    """
    Service de haut niveau.

    @ivar idservice: Identifiant du service.
    @ivar servicename: Nom du service.
    @ivar message: Message à afficher dans Vigiboard lorsque le service
        passe dans un état autre que OK.
    @ivar warning_threshold: Seuil à partir duquel le service passe de
        l'état OK à l'état WARNING.
    @ivar critical_threshold: Seuil à partir duquel le service passe de
        l'état WARNING à l'état CRITICAL.
    @ivar priority: Priorité à donner aux événements qui concernent
        ce service de haut niveau.
    @ivar impacts: Liste des services de haut niveau impactés par
        celui-ci.
    """
    __tablename__ = 'highlevelservice'
    __mapper_args__ = {
        'polymorphic_identity': 4,
        'extension': HlsMapperExt(),
    }

    idservice = Column(
        Integer,
        ForeignKey(
            SupItem.idsupitem,
            ondelete='CASCADE',
            onupdate='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        autoincrement=False, primary_key=True,
    )

    servicename = Column(
        Unicode(255),
        index=True, nullable=False,
        unique=True,
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

    _priorities = relation(HLSPriority,
        collection_class=attribute_mapped_collection('idstatename'),
        cascade="all,delete-orphan")
    priorities = association_proxy(
        '_priorities', 'priority', creator=HLSPriority)

    impacts = relation('ImpactedHLS', back_populates='hls',
                       lazy=True, cascade="all")

    def __init__(self, **kwargs):
        """Initialisation de l'objet."""
        super(HighLevelService, self).__init__(**kwargs)

    @classmethod
    def by_service_name(cls, servicename):
        """
        Renvoie le service de haut niveau dont le nom est L{servicename}.

        @param servicename: Nom du service de haut niveau voulu.
        @type servicename: C{unicode}
        @return: Le service de haut niveau demandé.
        @rtype: L{HighLevelService} ou None
        """
        return DBSession.query(cls).filter(
            cls.servicename == servicename).first()
