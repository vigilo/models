# -*- coding: utf-8 -*-
# Copyright (C) 2006-2021 CS GROUP - France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Table représentant la hiérarchie des groupes."""

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer
from sqlalchemy.orm import relation
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm.exc import NoResultFound

from vigilo.models.session import DeclarativeBase, DBSession
#from vigilo.models.tables.group import Group

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

    __tablename__ = 'vigilo_grouphierarchy'
    __table_args__ = (
        # Contrainte garantissant qu'un groupe
        # n'a qu'un seul parent.
        UniqueConstraint('idchild', 'hops'),
        {}
    )

    idparent = Column(
        Integer,
        ForeignKey(
            'vigilo_group.idgroup',
            ondelete='CASCADE',
            onupdate='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        nullable=False,
        primary_key=True,
    )

    idchild = Column(
        Integer,
        ForeignKey(
            'vigilo_group.idgroup',
            ondelete='CASCADE',
            onupdate='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
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
    def get_or_create(cls, hops, **kw):
        """
        création sans doublon
        """
        q = DBSession.query(cls)
        for k, v in kw.iteritems():
            q = q.filter(getattr(cls, k) == v)
        try:
            return q.one()
        except NoResultFound:
            gh = cls(hops=hops, **kw)
            DBSession.add(gh)
            return gh
