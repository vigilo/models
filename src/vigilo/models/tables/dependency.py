# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table dependency."""
from sqlalchemy import Column
from sqlalchemy.orm import relation
from sqlalchemy.types import Integer

from vigilo.models.session import DeclarativeBase, ForeignKey, DBSession
from vigilo.models.tables.supitem import SupItem

__all__ = ('Dependency', )

class Dependency(DeclarativeBase, object):
    """
    Marque un élément supervisé supitem1 comme dépendant d'un autre
    élément supervisé nommé supitem2 (vision fonctionnelle et non Nagios).

    @ivar idsupitem1: Identifiant de l'élément supervisé marqué comme
        dépendant d'un autre.
    @ivar supitem1: Instance d'élément supervisé marquée comme dépendante.
    @ivar idsupitem2: Identifiant de l'élement supervisé marqué comme
        dépendance d'un autre.
    @ivar supitem2: Instance d'élément supervisé marquée comme dépendance.
    """

    __tablename__ = 'dependency'

    idsupitem1 = Column(
        Integer,
        ForeignKey(
            SupItem.idsupitem,
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
            SupItem.idsupitem,
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        primary_key=True, autoincrement=False,
    )

    supitem2 = relation('SupItem', foreign_keys=[idsupitem2],
                    primaryjoin='SupItem.idsupitem == ' + \
                        'Dependency.idsupitem2')

    def __init__(self, **kwargs):
        super(Dependency, self).__init__(**kwargs)

    @classmethod
    def get_or_create(cls, supitem1, supitem2):
        """ création sans doublon
        """
        q = DBSession.query(cls
                        ).filter(cls.supitem1 == supitem1  
                        ).filter(cls.supitem2 == supitem2          
                        )
        if q.count() == 0:
            dep = cls(supitem1=supitem1, supitem2=supitem2)
            DBSession.add(dep)
            return dep
        else:
            return q.one()
    
    def __unicode__(self):
        return 'Dependency from %s on %s' % \
            (unicode(self.supitem1), unicode(self.supitem2))

