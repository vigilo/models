# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2016 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèle pour la table ImpactedHLS."""
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relation
from sqlalchemy.types import Integer

from vigilo.models.session import DeclarativeBase
from vigilo.models.tables.impactedpath import ImpactedPath
from vigilo.models.tables.service import HighLevelService

__all__ = ('ImpactedHLS', )

class ImpactedHLS(DeclarativeBase, object):
    """
    Marque un L{HighLevelService} comme impacté dans un chemin d'impactes.

    @ivar idpath: Identifiant du chemin d'impactes.
    @ivar path: Instance du chemin d'impactes.
    @ivar idhls: Identifiant du L{HighLevelService} impacté.
    @ivar hls: Instance du L{HighLevelService} impacté.
    @ivar distance: Distance à laquelle se trouve le L{HighLevelService}
        sur le chemin d'impactes par rapport à la source (le L{SupItem}
        à l'origine de l'impacte). Cet attribut est utilisé par VigiBoard
        pour n'afficher que les L{HighLevelService} situé tout au bout
        des chemins d'impactes liés à un L{CorrEvent} (ie. : ceux dont la
        distance est maximale sur le chemin).
    """

    __tablename__ = 'vigilo_impactedhls'


    idpath = Column(
        Integer,
        ForeignKey(
            ImpactedPath.idpath,
            onupdate='CASCADE',
            ondelete='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
        autoincrement=False,
    )

    path = relation('ImpactedPath', back_populates='impacted_hls', lazy=True)

    idhls = Column(
        Integer,
        ForeignKey(
            HighLevelService.idservice,
            onupdate='CASCADE',
            ondelete='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
        autoincrement=False,
    )

    hls = relation('HighLevelService', back_populates='impacts', lazy=True)

    distance = Column(
        Integer,
        primary_key=False, nullable=False,
    )

