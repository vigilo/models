# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table SupItem"""
from __future__ import absolute_import

from sqlalchemy import Column
from sqlalchemy.orm import relation, aliased
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.sql import functions

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from vigilo.models.secondary_tables import SUPITEM_TAG_TABLE
from vigilo.models.session import DBSession

__all__ = ('SupItem', )

class SupItem(DeclarativeBase, object):
    """
    Classe abstraite qui gère un objet supervisé.

    @ivar idsupitem: Identifiant de l'objet supervisé.
    @ivar tags: Libellés attachés à cet objet.
    """
    __tablename__ = bdd_basename + 'supitem'

    idsupitem = Column(
        Integer,
        primary_key=True, autoincrement=True,
    )

    _itemtype = Column(
        'itemtype', Unicode(16),
        index=True,
    )

    tags = relation('Tag', secondary=SUPITEM_TAG_TABLE,
        back_populates='supitems', lazy=True)

    __mapper_args__ = {'polymorphic_on': _itemtype}


    def impacted_hls(self, *args):
        """
        Renvoie une requête portant sur les services de haut niveau impactés.
        
        @param *args: Liste d'éléments à récupérer dans la requête.
        @type *args: Une C{DeclarativeBase} ou une liste de C{Column}s.
        @return: Une C{Query} portant sur les éléments demandés.
        @rtype: C{sqlalchemy.orm.query.Query}.
        """
        from vigilo.models import ServiceHighLevel, ImpactedHLS, ImpactedPath

        if not args:
            args = [ServiceHighLevel]

        subquery = DBSession.query(
            functions.max(ImpactedHLS.distance).label('distance'),
            ImpactedHLS.idpath
        ).join(
            (ImpactedPath, ImpactedPath.idpath == ImpactedHLS.idpath)
        ).group_by(ImpactedHLS.idpath).subquery()

        ends = aliased(ImpactedHLS, subquery)

        services_query = DBSession.query(*args).distinct(
            ).join(
                ImpactedHLS,
                (ends, ends.idpath == ImpactedHLS.idpath),
            ).filter(ImpactedHLS.distance == ends.distance
            )

        return services_query
 
 
    @classmethod
    def get_supitem(cls, hostname, servicename):
        """
        Récupère dans la BDD l'identifiant de l'item (host ou service)
        correspondant à ce hostname et à ce servicename. 
        Lorsque le paramètre servicename vaut None, l'item est alors un host. 
        Lorsque le paramètre hostname vaut None, l'item est un SHN.
        Sinon, l'item est un SBN.
            
        @param hostname: Nom du host.
        @type hostname: C{str}
        @param servicename: Nom du service.
        @type servicename: C{str}
        @return: L'identifiant d'un host, un SHN, ou un SBN.
        @rtype: C{int}
        """  
        from vigilo.models import Host, ServiceHighLevel, ServiceLowLevel
        from sqlalchemy.sql.expression import and_
        
        # Si le nom du service vaut None, l'item est un hôte.
        if not servicename:
            host = DBSession.query(Host.idhost
                        ).filter(Host.name == hostname
                        ).first()
                    
            if host:
                return host.idhost
    
            LOGGER.error(_('Got a reference to a non configured ' +
                    'host (%r)') % (hostname, ))
            return None
        
        # Lorsque l'item est un service de haut niveau.
        if not hostname:
            service = DBSession.query(ServiceHighLevel.idservice
                        ).filter(ServiceHighLevel.servicename == servicename,
                        ).first()
                    
            if service:
                return service.idservice
                
            LOGGER.error(_('Got a reference to a non configured ' +
                    'high level service (%r)') % (servicename, ))
            return None
        
        # Sinon, l'item est un service de bas niveau.
        service = DBSession.query(ServiceLowLevel.idservice
                    ).join(
                        (Host, ServiceLowLevel.idhost == Host.idhost)
                    ).filter(
                         and_(
                            ServiceLowLevel.servicename == servicename,
                            Host.name == hostname
                        )
                    ).first()
                
        if service:
            return service.idservice
                
        LOGGER.error(_('Got a reference to a non configured ' +
                'low level service (%r, %r)') % (hostname, servicename))
        return None


    def __init__(self, **kwargs):
        """Initialise un objet supervisé."""
        super(SupItem, self).__init__(**kwargs)

