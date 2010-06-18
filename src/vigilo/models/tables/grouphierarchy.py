# -*- coding: utf-8 -*-
"""Table représentant la hiérarchie des groupes."""

from sqlalchemy import Column
from sqlalchemy.types import Integer
from sqlalchemy.orm import relation

from vigilo.models.session import DeclarativeBase, ForeignKey, DBSession
from vigilo.models.tables.group import Group

class GroupHierarchy(DeclarativeBase, object):
    """
    Table permettant de représenter la hiérarchie des C{*Group}es.
    Le graphe représenté par cette table est transitif et réflexif.

    @ivar idparent: Identifiant du groupe parent.
    @ivar idchild: Identifiant du groupe fils.
    @ivar hops: Distance séparant le groupe parent du groupe fils.
        Un groupe est distant de lui-même à une distance de 0,
        de ses fils à une distance de 1, de ses sous-fils à une
        distance de 2, etc.
    @ivar parent: Instance du groupe parent.
    @ivar child: Instance du groupe fils.
    """

    __tablename__ = 'grouphierarchy'

    idparent = Column(
        Integer,
        ForeignKey(
            Group.idgroup,
            ondelete='CASCADE',
            onupdate='CASCADE',
        ),
        nullable=False,
        primary_key=True,
    )

    idchild = Column(
        Integer,
        ForeignKey(
            Group.idgroup,
            ondelete='CASCADE',
            onupdate='CASCADE',
        ),
        nullable=False,
        primary_key=True,
    )

    hops = Column(
        Integer,
        nullable=False,
    )

    parent = relation('Group', foreign_keys=[idparent],
                primaryjoin='Group.idgroup == GroupHierarchy.idparent')

    child = relation('Group', foreign_keys=[idchild],
                primaryjoin='Group.idgroup == GroupHierarchy.idchild')

    def __init__(self, **kwargs):
        """
        Initialise l'instance avec les informations sur une partie de la
        hiérarchie des groupes.
        
        @param kwargs: Un dictionnaire avec les informations
            sur la hiérarchie des groupes.
        @type kwargs: C{dict}
        """
        super(GroupHierarchy, self).__init__(**kwargs)

    @classmethod
    def get_or_create(cls, parent, child, hops):
        """
        création sans doublon
        """
        q = DBSession.query(cls
                        ).filter(cls.parent == parent  
                        ).filter(cls.child == child          
                        )
        if q.count() == 0:
            gh = cls(parent=parent, child=child, hops=hops)
            DBSession.add(gh)
            return gh
        else:
            return q.one()
    
