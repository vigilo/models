# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2014 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèle pour la table ImpactedPath."""
from sqlalchemy import Column
from sqlalchemy.orm import relation
from sqlalchemy.types import Integer

from vigilo.models.session import DeclarativeBase, ForeignKey
from vigilo.models.tables.supitem import SupItem

__all__ = ('ImpactedPath', )

class ImpactedPath(DeclarativeBase, object):
    """
    Cette classe contient les données relatives à un chemin d'impactes.

    @ivar idpath: Identifiant auto-généré du chemin.
    @ivar impacted_hls: Liste des L{HighLevelService} impactés présents
        sur le chemin.
    @ivar idsupitem: Identifiant de l'élément supervisé à l'origine du
        chemin d'impactes.
    @ivar supitem: Instance de l'élément supervisé à l'origine du chemin
        d'impactes.
    """

    __tablename__ = 'impactedpath'

    idpath = Column(
        Integer,
        primary_key=True, autoincrement=True,
    )

    impacted_hls = relation('ImpactedHLS', back_populates='path',
                            lazy=True, cascade="all")

    idsupitem = Column(
        Integer,
        ForeignKey(
            SupItem.idsupitem,
            ondelete='CASCADE',
            onupdate='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        nullable=False,
    )

    supitem = relation('SupItem')

