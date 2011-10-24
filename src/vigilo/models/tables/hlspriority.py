# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2011 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèle pour la table HLSPriority"""
from sqlalchemy import Column
from sqlalchemy.types import Unicode, Integer
from sqlalchemy.orm import relation, synonym
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
    def __init__(cls, *args, **kw):
        if getattr(cls, '_decl_class_registry', None) is None:
            return

        super(HLSPriorityIndexMeta, cls).__init__(*args, **kw)
        Index(
            'ix_%s_key' % cls.__tablename__,
            cls.idhls, cls.idstatename,
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
        """
        if not isinstance(hls, int):
            hls = hls.idservice
        if isinstance(statename, StateName):
            statename = statename.idstatename
        elif isinstance(statename, basestring):
            statename = StateName.statename_to_value(unicode(statename))
        return DBSession.query(cls).filter(cls.idhls == hls
            ).filter(cls.idstatename == statename).first()
