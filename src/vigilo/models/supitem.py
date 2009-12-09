# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table SupItem"""
from __future__ import absolute_import

from sqlalchemy import Column
from sqlalchemy.orm import relation
from sqlalchemy.types import Integer, Unicode

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from vigilo.models.secondary_tables import SUPITEM_TAG_TABLE

__all__ = ('SupItem', )

class SupItem(DeclarativeBase, object):
    __tablename__ = bdd_basename + 'supitem'

    idsupitem = Column(
        Integer,
        primary_key=True, autoincrement=True,
    )

    _itemtype = Column(
        'itemtype', Unicode(16),
        index=True,
    )

    tags = relation('Tag', secondary=SUPITEM_TAG_TABLE,
        back_populates='supitems', lazy='dynamic')

    impacted_paths = relation('ImpactedPath', back_populates='supitem',
        lazy='dynamic')

    __mapper_args__ = {'polymorphic_on': _itemtype}

    def __init__(self, **kwargs):
        super(SupItem, self).__init__(**kwargs)

