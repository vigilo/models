# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table SupItem"""
from __future__ import absolute_import

from sqlalchemy import Column
from sqlalchemy.orm import relation, aliased
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.sql import functions
from sqlalchemy.sql.expression import and_

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from vigilo.models.secondary_tables import SUPITEM_TAG_TABLE
from vigilo.models.session import DBSession

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
        back_populates='supitems', lazy=True)

    __mapper_args__ = {'polymorphic_on': _itemtype}

    def impacted_hls(self, *args):
        from vigilo.models import ServiceHighLevel, ImpactedHLS, ImpactedPath

        if not args:
            args = [ServiceHighLevel]

        subquery = DBSession.query(
            functions.max(ImpactedHLS.distance).label('distance'),
            ImpactedHLS.idpath
        ).join(
            (ImpactedPath, ImpactedPath.idpath == ImpactedHLS.idpath)
        ).group_by(ImpactedHLS.idpath).subquery()

        ends = aliased(ImpactedHLS, subquery)

        services_query = DBSession.query(*args).distinct(
            ).join(
                ImpactedHLS,
                (ends, ends.idpath == ImpactedHLS.idpath),
            ).filter(ImpactedHLS.distance == ends.distance
            )

        return services_query

    def __init__(self, **kwargs):
        super(SupItem, self).__init__(**kwargs)

