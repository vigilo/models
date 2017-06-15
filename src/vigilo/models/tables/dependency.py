# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2016 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèle pour la table dependency."""
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relation
from sqlalchemy.types import Integer

from vigilo.models.session import DeclarativeBase
from vigilo.models.tables.supitem import SupItem
from vigilo.models.tables.dependencygroup import DependencyGroup

__all__ = ('Dependency', )

class Dependency(DeclarativeBase, object):
    """
    Gère une dépendance (logique ou fonctionnelle).
    Le type de dépendance est donné dans L{DependencyGroup}.

    @ivar idgroup: Identifiant du groupe de dépendances
        auquel cette dépendance appartient.
    @ivar group: Instance du groupe de dépendances
        auquel cette dépendance appartient.
    @ivar idsupitem: Identifiant de l'élément supervisé
        qui constitue la dépendance.
    @ivar supitem: Instance de l'élément supervisé
        qui constitue la dépendance.
    @ivar weight: Poids de l'élément supervisé constituant
        la dépendance dans un état nominal.
    @ivar warning_weight: Poids de l'élément supervisé
        constituant la dépendance dans un état dégradé.
    """

    __tablename__ = 'vigilo_dependency'

    idgroup = Column(
        Integer,
        ForeignKey(
            DependencyGroup.idgroup,
            ondelete='CASCADE',
            onupdate='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
        autoincrement=False,
    )

    group = relation('DependencyGroup')

    idsupitem = Column(
        Integer,
        ForeignKey(
            SupItem.idsupitem,
            ondelete='CASCADE',
            onupdate='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
        autoincrement=False,
    )

    supitem = relation('SupItem')

    distance = Column(
        Integer,
        primary_key=False,
        nullable=True,
    )

    # Uniquement pour les dépendances de type HLS.
    weight = Column(
        Integer,
        primary_key=False,
        nullable=True,
    )

    # Uniquement pour les dépendances de type HLS.
    warning_weight = Column(
        Integer,
        primary_key=False,
        nullable=True,
    )

    def __init__(self, **kwargs):
        super(Dependency, self).__init__(**kwargs)

    def __unicode__(self):
        return 'Dependency from %s on %s' % (
            unicode(self.group.dependent),
            unicode(self.supitem),
        )
