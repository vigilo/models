# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2015 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèle pour la table HLSPriority"""
from sqlalchemy import Column
from sqlalchemy.types import Integer
from sqlalchemy.orm import relation
from sqlalchemy.schema import Index

from vigilo.models.session import DeclarativeBase, DBSession, \
                                    ForeignKey, PrefixedTables
from vigilo.models.tables.statename import StateName

class HLSPriorityIndexMeta(PrefixedTables):
    """
    Cette méta-classe ajoute un index sur les colonnes "name"
    et "idsupitem", utilisée par VigiConf lors de la mise à jour
    des entrées de la table L{ConfItem}.
    """
    def __init__(mcs, *args, **kw):
        if getattr(mcs, '_decl_class_registry', None) is None:
            return

        super(HLSPriorityIndexMeta, mcs).__init__(*args, **kw)
        Index(
            'ix_%s_key' % mcs.__tablename__,
            mcs.idhls, mcs.idstatename,
            unique=True
        )

class HLSPriorityMixin(object):
    """
    Ce mixin permet simplement d'intégrer la méta-classe,
    afin d'éviter un conflit entre méta-classes dans ConfItem.
    """
    __metaclass__ = HLSPriorityIndexMeta

class HLSPriority(DeclarativeBase, HLSPriorityMixin):
    """
    Un tag associé soit à un élément supervisé.

    @ivar name: Nom du tag.
    @ivar value: Valeur associée au tag.
    @ivar supitems: Liste des éléments supervisés (L{SupItem}s) auxquels
        le tag est rattaché.
    """

    __tablename__ = 'hlspriority'

    idhls = Column(
        Integer,
        ForeignKey(
            'highlevelservice.idservice',
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
        autoincrement=True,
        index=True,
        nullable=False,
    )

    idstatename = Column(
        Integer,
        ForeignKey(
            'statename.idstatename',
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
        autoincrement=False,
        index=True,
        nullable=False,
    )

    priority = Column(
        Integer,
        primary_key=False,
        nullable=False,
    )

    hls = relation('HighLevelService', lazy=True)

    def __init__(self, statename, priority):
        """
        Associe une nouvelle priorité à un service de haut niveau
        en fonction de son état.

        @param statename: État pour lequel la priorité doit être modifiée.
        @type statename: C{int} or C{basestr} or L{StateName}
        @param priority: Nouvelle priorité pour ce service de haut niveau
            et cet état.
        @type priority: C{int}
        """
        if isinstance(statename, basestring):
            statename = StateName.statename_to_value(statename)
        elif isinstance(statename, StateName):
            statename = statename.idstatename

        super(HLSPriority, self).__init__(
            idstatename=statename,
            priority=priority)

    def __unicode__(self):
        """
        Représentation unicode du tag.

        @return: Le nom du tag.
        @rtype: C{unicode}
        """
        return self.name

    @classmethod
    def by_hls_and_statename(cls, hls, statename):
        """
        Retourne la priorité associée à un service de haut niveau
        pour un état donné.

        @param hls: Service de haut niveau dont on souhaite connaître
            la priorité.
        @type hls: C{int} or L{vigilo.models.tables.HighLevelService}
        @param statename: État pour lequel la priorité doit être retournée.
        @type statename: C{int} or C{basestr} or L{StateName}
        @return: Priorité associée au service de haut niveau
            en fonction de l'état donné.
        @rtype: L{HLSPriority}
        """
        if not isinstance(hls, int):
            hls = hls.idservice
        if isinstance(statename, StateName):
            statename = statename.idstatename
        elif isinstance(statename, basestring):
            statename = StateName.statename_to_value(unicode(statename))
        return DBSession.query(cls).filter(cls.idhls == hls
            ).filter(cls.idstatename == statename).first()
