# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table UserGroup"""
from __future__ import absolute_import

from sqlalchemy.orm import mapper
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.types import UnicodeText
from sqlalchemy.orm import relation

from .vigilo_bdd_config import bdd_basename, DeclarativeBase, metadata
from .user import User

__all__ = ('UserGroup', )

user_group_table = Table('usertousergroups', metadata,
    Column('username', UnicodeText, ForeignKey(
        bdd_basename + 'user.user_name',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('groupname', UnicodeText, ForeignKey(
        bdd_basename + 'usergroup.group_name',
        onupdate="CASCADE", ondelete="CASCADE"))
)

class UserGroup(DeclarativeBase):
    """User groups, used eg. to organize users by services, privileges, etc."""

    __tablename__ = bdd_basename + 'usergroup'

    # TG2 expects this name.
    group_name = Column(
        UnicodeText(),
        primary_key=True)

    users = relation('User', secondary=user_group_table, backref='groups')

    def __unicode__(self):
        return self.group_name

