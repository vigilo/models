# -*- coding: utf-8 -*-
from sqlalchemy import Column
from sqlalchemy.types import Unicode, Integer
from sqlalchemy.orm import relation, backref
from sqlalchemy.schema import UniqueConstraint

from vigilo.models.session import DeclarativeBase, ForeignKey
from vigilo.models.tables.group import Group

class GroupHierarchy(DeclarativeBase):
    __tablename__ = 'grouphierarchy'

    idparent = Column(
        Integer,
        ForeignKey(
            Group.idgroup,
            ondelete='CASCADE',
            onupdate='CASCADE',
        ),
        primary_key=True,
    )

    idchild = Column(
        Integer,
        ForeignKey(
            Group.idgroup,
            ondelete='CASCADE',
            onupdate='CASCADE',
        ),
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

