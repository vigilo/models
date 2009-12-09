# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Dependency."""
from __future__ import absolute_import

from sqlalchemy import ForeignKey, Column
from sqlalchemy.orm import relation
from sqlalchemy.types import Unicode, Integer

from .vigilo_bdd_config import bdd_basename, DeclarativeBase

__all__ = ('Dependency', )

class Dependency(DeclarativeBase, object):
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

    __tablename__ = bdd_basename + 'dependency'

    idsupitem1 = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'supitem.idsupitem',
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        primary_key=True, autoincrement=False,
    )

    supitem1 = relation('SupItem', foreign_keys=[idsupitem1],
                    primaryjoin='SupItem.idsupitem == ' + \
                        'Dependency.idsupitem1')

    idsupitem2 = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'supitem.idsupitem',
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        primary_key=True, autoincrement=False,
    )

    supitem2 = relation('SupItem', foreign_keys=[idsupitem2],
                    primaryjoin='SupItem.idsupitem == ' + \
                        'Dependency.idsupitem2')

    def __init__(self, **kwargs):
        super(Dependency, self).__init__(**kwargs)

