# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table ImpactedHLS."""
from __future__ import absolute_import

from sqlalchemy import ForeignKey, Column
from sqlalchemy.orm import relation
from sqlalchemy.types import Integer

from .vigilo_bdd_config import bdd_basename, DeclarativeBase

__all__ = ('ImpactedHLS', )

class ImpactedHLS(DeclarativeBase, object):
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

    __tablename__ = bdd_basename + 'impactedhls'


    idpath = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'impactedpath.idpath',
            onupdate='CASCADE', ondelete='CASCADE',
        ),
        primary_key=True, autoincrement=False,
    )

    path = relation('ImpactedPath', back_populates='impacted_hls', lazy=True)

    idhls = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'servicehighlevel.idservice',
            onupdate='CASCADE', ondelete='CASCADE',
        ),
        primary_key=True, autoincrement=False,
    )

    hls = relation('ServiceHighLevel', back_populates='impacts', lazy=True)

    distance = Column(
        Integer,
        primary_key=False, nullable=False,
    )

