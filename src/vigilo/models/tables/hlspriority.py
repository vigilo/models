# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2021 CS GROUP - France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèle pour la table HLSPriority"""
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer
from sqlalchemy.orm import relation
from sqlalchemy.schema import Index
from sqlalchemy.ext.declarative import declared_attr

from vigilo.models.session import DeclarativeBase, DBSession
from vigilo.models.tables.statename import StateName

class HLSPriority(DeclarativeBase):
    """
    Un tag associé soit à un élément supervisé.

    @ivar name: Nom du tag.
    @ivar value: Valeur associée au tag.
    @ivar supitems: Liste des éléments supervisés (L{SupItem}s) auxquels
        le tag est rattaché.
    """

    __tablename__ = 'vigilo_hlspriority'

    idhls = Column(
        Integer,
        ForeignKey(
            'vigilo_highlevelservice.idservice',
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
            StateName.idstatename,
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

    __table_args__ = (
        Index(
            'ix_%s_key' % __tablename__,
            idhls,
            idstatename,
            unique=True
        ),
    )

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
