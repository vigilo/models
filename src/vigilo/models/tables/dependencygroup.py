# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2015 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèle pour la table dependency."""
from sqlalchemy import Column
from sqlalchemy.orm import relation
from sqlalchemy.types import Integer, Unicode

from vigilo.models.session import DeclarativeBase, ForeignKey
from vigilo.models.tables.supitem import SupItem

__all__ = ('DependencyGroup', )

class DependencyGroup(DeclarativeBase, object):
    """
    Gère un groupe de dépendances associées
    à un élément du parc.

    @ivar idgroup: Identifiant du groupe de dépendances.
    @ivar operator: Opération effectuée sur le groupe de dépendances.
        Il peut s'agir de "&" (poids = min(poids_dependences))
        ou bien de "|" (poids = max(poids_dependences))
        ou bien de "+" (poids = somme(poids_dependences)).
        Pour le moment, cet attribut n'a de sens que pour les services
        de haut niveau et est ignoré pour les autres types d'éléments.
    @ivar iddependent: Identifiant de l'élément supervisé sur lequel
        portent les dépendances (i.e. : l'élément dépendant).
    @ivar dependent: Instance de l'élément supervisé dépendant.
    @ivar role: Le rôle du groupe de dépendances :
        - soit "hls" pour les dépendances d'un service de haut niveau
        - ou "topology" pour des dépendances topologiques.
    """

    __tablename__ = 'dependencygroup'

    idgroup = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    operator = Column(
        Unicode(1),
        nullable=False,
    )

    iddependent = Column(
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

    role = Column(
        Unicode(16),
        nullable=False,
    )

    dependent = relation('SupItem')

    def __init__(self, **kwargs):
        super(DependencyGroup, self).__init__(**kwargs)

    def __unicode__(self):
        return 'DependencyGroup for %s' % unicode(self.dependent)
