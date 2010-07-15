# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Service"""
from sqlalchemy import Column
from sqlalchemy.types import UnicodeText, Unicode, Integer
from sqlalchemy.orm import relation
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import EXT_CONTINUE

from vigilo.models.session import DBSession, ForeignKey
from vigilo.models.tables.supitem import SupItem, SupItemMapperExt
from vigilo.models.tables.host import Host

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

    @ivar idservice: Identifiant du service.
    @ivar op_dep: Le type d'opération à appliquer aux dépendances de ce
        service de haut niveau ('+', '&' ou '|').
    @ivar groups: Liste des groupes de services auxquels ce service appartient.
    @ivar dependancies: Liste des services dont ce service dépend.
        Pour les services techniques, cette liste est toujours vide.
    @note: Le nom du service a été déplacé au niveau des classes filles
        afin de permettre l'ajout de contraintes SQL supplémentaires
        (ex: unicité du nom du service pour un hôte donné).
    """
    __tablename__ = 'service'

    idservice = Column(
        Integer,
        ForeignKey(
            SupItem.idsupitem,
            onupdate='CASCADE', ondelete='CASCADE',
        ),
        primary_key=True, autoincrement=False,
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

    def __repr__(self):
        try:
            return "<%s \"%s\">" % (self.__class__.__name__,
                                    str(self.servicename))
        except Exception:
            return super(Service, self).__repr__()


class LowLevelService(Service):
    """
    Service de bas niveau (service technique).

    @ivar idservice: Identifiant du service.
    @ivar servicename: Nom du service.
    @ivar idhost: Identifiant de l'L{Host} sur lequel ce service est configuré.
    @ivar host: Instande de l'L{Host} sur lequel ce service est configuré.
    @ivar command: Commande à exécuter pour vérifier l'état du service.
    @ivar weight: Poids affecté à ce service pour le calcul de l'état
        des services de haut niveau (L{HighLevelService}).
    """
    __tablename__ = 'lowlevelservice'
    __table_args__ = (
        UniqueConstraint('servicename', 'idhost'),
        {}
    )
    __mapper_args__ = {
        'polymorphic_identity': u'lowlevel',
       'extension': LlsMapperExt(),
    }

    idservice = Column(
        Integer,
        ForeignKey(
            Service.idservice,
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        autoincrement=False, primary_key=True,
    )

    servicename = Column(
        Unicode(255),
        index=True, nullable=False,
    )

    idhost = Column(
        Integer,
        ForeignKey(
            Host.idhost,
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        nullable=False,
    )

    host = relation('Host', foreign_keys=[idhost],
        primaryjoin='LowLevelService.idhost == Host.idsupitem')

    command = Column(
        UnicodeText,
        default=u'', nullable=False,
    )

    weight = Column(
        Integer,
        nullable=False,
    )


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
        return "%s (%s)" % (self.servicename, self.host.name)
    
    def __repr__(self):
        try:
            return "<%s \"%s\" on \"%s\">" % (self.__class__.__name__,
                            str(self.servicename), str(self.host.name))
        except Exception:
            return super(LowLevelService, self).__repr__()


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
    @ivar weight: Poids courant du service de haut niveau. Vaut None
        si le poids n'a pas encore été calculé (à l'initialisation
        par exemple).
    @ivar priority: Priorité à donner aux événements qui concernent
        ce service de haut niveau.
    @ivar impacts: Liste des services de haut niveau impactés par
        celui-ci.
    """
    __tablename__ = 'highlevelservice'
    __mapper_args__ = {
        'polymorphic_identity': u'highlevel',
        'extension': HlsMapperExt(),
    }

    idservice = Column(
        Integer,
        ForeignKey(
            Service.idservice,
            ondelete='CASCADE', onupdate='CASCADE',
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

    weight = Column(
        Integer,
        nullable=True,
    )

    priority = Column(
        Integer,
        nullable=False,
    )

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

