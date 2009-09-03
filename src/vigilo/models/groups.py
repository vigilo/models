# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Groups"""
from __future__ import absolute_import

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.types import UnicodeText, Integer
from sqlalchemy.orm import relation, backref
from .session import DBSession

from .vigilo_bdd_config import bdd_basename, DeclarativeBase, metadata

GROUP_PERMISSION_TABLE = Table(
    bdd_basename + 'grouppermissions', metadata,
    Column('groupname', UnicodeText, ForeignKey(
                bdd_basename + 'groups.name',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
    Column('idpermission', Integer, ForeignKey(
                bdd_basename + 'permission.idpermission',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False)
)

class Groups(DeclarativeBase):
    __tablename__ = bdd_basename + 'groups'

    name = Column(
        UnicodeText(),
        primary_key=True, nullable=False)

    _parent = Column(
        'parent', UnicodeText(),
        ForeignKey(bdd_basename + 'groups.name'),
        index=True)

    children = relation('Groups', backref=backref('parent', remote_side=[name]))

    permissions = relation('Permission',
        secondary=GROUP_PERMISSION_TABLE, backref='groups')


    @classmethod
    def by_name(cls, groupname):
        """Returns the group whose name is ``groupname``."""
        return DBSession.query(cls).filter(cls.name==groupname).first()

