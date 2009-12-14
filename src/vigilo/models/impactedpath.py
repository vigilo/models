# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table ImpactedPath."""
from __future__ import absolute_import

from sqlalchemy import ForeignKey, Column
from sqlalchemy.orm import relation
from sqlalchemy.types import Unicode, Integer

from .vigilo_bdd_config import bdd_basename, DeclarativeBase

__all__ = ('ImpactedPath', )

class ImpactedPath(DeclarativeBase, object):
    """
    Marque un élément supervisé supitem1 comme dépendant d'un autre
    élément supervisé nommé supitem2.

    @ivar idsupitem1: Identifiant de l'élément supervisé marqué comme
        dépendant d'un autre.
    @ivar supitem1: Instance d'élément supervisé marquée comme dépendante.
    @ivar idsupitem2: Identifiant de l'élement supervisé marqué comme
        dépendance d'un autre.
    @ivar supitem2: Instance d'élément supervisé marquée comme dépendance.
    """

    __tablename__ = bdd_basename + 'impactedpath'

    idpath = Column(
        Integer,
        primary_key=True, autoincrement=True,
    )

    impacted_hls = relation('ImpactedHLS', back_populates='path', lazy=True,
#        primaryjoin='ImpactedHLS.idpath == ImpactedPath.idpath',
        )

    idsupitem = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'supitem.idsupitem',
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        nullable=False,
    )

    supitem = relation('SupItem', back_populates='impacted_paths', lazy=True)

