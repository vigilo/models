# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table dependency."""
from sqlalchemy import Column
from sqlalchemy.orm import relation
from sqlalchemy.types import Integer

from vigilo.models.session import DeclarativeBase, ForeignKey, DBSession
from vigilo.models.tables.supitem import SupItem
from vigilo.models.tables.dependencygroup import DependencyGroup

__all__ = ('Dependency', )

class Dependency(DeclarativeBase, object):
    """
    """

    __tablename__ = 'dependency'

    idgroup = Column(
        Integer,
        ForeignKey(
            DependencyGroup.idgroup,
            ondelete='CASCADE',
            onupdate='CASCADE',
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
        ),
        primary_key=True,
        autoincrement=False,
    )

    supitem = relation('SupItem')

    def __init__(self, **kwargs):
        super(Dependency, self).__init__(**kwargs)

    def __unicode__(self):
        return 'Dependency from %s on %s' % (
            unicode(self.group.dependent),
            unicode(self.supitem),
        )
