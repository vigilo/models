# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2011 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèle pour la table SupItem"""
from sqlalchemy import Column
from sqlalchemy.orm import relation, aliased
from sqlalchemy.orm.interfaces import MapperExtension
from sqlalchemy.orm import EXT_CONTINUE
from sqlalchemy.types import Integer
from sqlalchemy.sql import functions
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.associationproxy import association_proxy

from vigilo.models.session import DeclarativeBase, DBSession
from vigilo.models.tables.secondary_tables import SUPITEM_GROUP_TABLE
from vigilo.models.tables.tag import Tag

__all__ = ('SupItem', 'SupItemMapperExt')


class SupItemMapperExt(MapperExtension):
    """
    Quand un SupItem est ajouté en base, son état par défaut est OK. Ce
    comportement est similaire à celui de Nagios. Si l'état n'est pas OK en
    réalité, Nagios le détectera et enverra une notification, ce qui mettra à
    jour l'état en base de données.

    Fonctionnalité SQLAlchemy utilisée :
    http://www.sqlalchemy.org/docs/05/reference/orm/interfaces.html#sqlalchemy.orm.interfaces.MapperExtension
    """
    def after_insert(self, mapper, connection, instance):
        from vigilo.models.tables.state import State
        from vigilo.models.tables.statename import StateName
        s = State(idsupitem=instance.idsupitem,
                         state=StateName.statename_to_value(u"OK"),
                         message=u"")
        DBSession.merge(s)
        return EXT_CONTINUE


class SupItem(DeclarativeBase, object):
    """
    Classe abstraite qui gère un objet supervisé.

    @ivar idsupitem: Identifiant de l'objet supervisé.
    @ivar _itemtype: Type d'élément supervisé (host, lowlevelservice,
        highlevelservice).
    @ivar tags: Libellés attachés à cet objet.
    """
    __tablename__ = 'supitem'
    __mapper_args__ = {'extension': SupItemMapperExt()}

    idsupitem = Column(
        Integer,
        primary_key=True, autoincrement=True,
    )

    _itemtype = Column(
        'itemtype', Integer,
        index=True,
        nullable=False,
        autoincrement=False,
    )

    _tags = relation(Tag,
        collection_class=attribute_mapped_collection('name'),
        cascade="all,delete-orphan")
    tags = association_proxy('_tags', 'value', creator=Tag)

    groups = relation('SupItemGroup', secondary=SUPITEM_GROUP_TABLE,
                back_populates='supitems', lazy=True)

    state = relation('State', back_populates="supitem", cascade="all",
                     lazy=True, uselist=False)

    __mapper_args__ = {'polymorphic_on': _itemtype}


    def impacted_hls(self, *args):
        """
        Renvoie une requête portant sur les services de haut niveau impactés.

        @param args: Liste d'éléments à récupérer dans la requête.
        @type args: Une C{DeclarativeBase} ou une liste de C{Column}s.
        @return: Une C{Query} portant sur les éléments demandés.
        @rtype: C{sqlalchemy.orm.query.Query}
        """
        from vigilo.models.tables import HighLevelService, \
                                            ImpactedHLS, ImpactedPath

        if not args:
            args = [HighLevelService]

        imp_hls1 = aliased(ImpactedHLS)
        imp_hls2 = aliased(ImpactedHLS)

        subquery = DBSession.query(
            functions.max(imp_hls1.distance).label('distance'),
            imp_hls1.idpath
        ).join(
            (ImpactedPath, ImpactedPath.idpath == imp_hls1.idpath)
        ).filter(ImpactedPath.idsupitem == self.idsupitem
        ).group_by(imp_hls1.idpath).subquery()

        services_query = DBSession.query(*args).distinct(
        ).join(
            (imp_hls2, HighLevelService.idservice == imp_hls2.idhls),
            (subquery, subquery.c.idpath == imp_hls2.idpath),
        ).filter(imp_hls2.distance == subquery.c.distance)

        return services_query


    @classmethod
    def get_supitem(cls, hostname, servicename):
        """
        Récupère dans la BDD l'identifiant de l'item (host ou service)
        correspondant à ce hostname et à ce servicename.
        Lorsque le paramètre servicename vaut None, l'item est alors un host.
        Lorsque le paramètre hostname vaut None, l'item est un SHN.
        Sinon, l'item est un SBN.

        Remarque de AB: j'aurais bien vu un nom du genre `by_names()` plutôt,
        mais bon, on va pas tout casser juste pour faire joli.

        @param hostname: Nom du host.
        @type hostname: C{str}
        @param servicename: Nom du service.
        @type servicename: C{str}
        @return: L'identifiant d'un host, un SHN, ou un SBN.
        @rtype: C{int}
        """
        from vigilo.models.tables import Host, HighLevelService, \
                                            LowLevelService
        from sqlalchemy.sql.expression import and_

        # Si le nom du service vaut None, l'item est un hôte.
        if not servicename:
            return DBSession.query(Host.idhost
                        ).filter(Host.name == hostname
                        ).scalar()

        # Lorsque l'item est un service de haut niveau.
        if not hostname:
            return DBSession.query(HighLevelService.idservice
                        ).filter(HighLevelService.servicename == servicename,
                        ).scalar()

        # Sinon, l'item est un service de bas niveau.
        return DBSession.query(LowLevelService.idservice
                    ).join(
                        (Host, LowLevelService.idhost == Host.idhost)
                    ).filter(
                         and_(
                            LowLevelService.servicename == servicename,
                            Host.name == hostname
                        )
                    ).scalar()


    def is_allowed_for(self, user, perm_type="r"):
        """
        Vérifie que l'utilisateur fourni en paramètre à le droit d'accéder au
        supitem, avec la permission optionnellement spécifiée.

        @todo: probablement à optimiser, ça fait beaucoup de requêtes.
        @todo: pour le moment, le paramètre perm_type n'est pas utilisé.

        @param user: L'utilisateur dont la permission est à tester
        @type  user: L{User}
        @param perm_type: Type d'accès, par défaut "r"
        @type  perm_type: C{str}
        @return: True si l'accès est autorisé, False sinon.
        @rtype: C{bool}
        """
        if u"managers" in [g.group_name for g in user.usergroups]:
            return True
        direct_groups = [sg[0] for sg in user.supitemgroups() if sg[1]]
        for group in self.groups:
            if group.idgroup in direct_groups:
                return True
        return False


    def __init__(self, **kwargs):
        """Initialise un objet supervisé."""
        super(SupItem, self).__init__(**kwargs)
