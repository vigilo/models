# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table dependency."""
from sqlalchemy import Column
from sqlalchemy.orm import relation
from sqlalchemy.types import Integer, Unicode

from vigilo.models.session import DeclarativeBase, ForeignKey, DBSession
from vigilo.models.tables.supitem import SupItem

__all__ = ('DependencyGroup', )

class DependencyGroup(DeclarativeBase, object):
    """
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
        ),
        nullable=False,
    )

    dependent = relation('SupItem')

    def __init__(self, **kwargs):
        super(DependencyGroup, self).__init__(**kwargs)

    def __unicode__(self):
        return 'DependencyGroup for %s' % unicode(self.dependent)
