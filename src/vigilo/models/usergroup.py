# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table UserGroup"""
from __future__ import absolute_import

from sqlalchemy import Column
from sqlalchemy.types import Unicode, Integer
from sqlalchemy.orm import relation, backref

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .session import DBSession
from .secondary_tables import USERGROUP_PERMISSION_TABLE, USER_GROUP_TABLE

__all__ = ('UserGroup', )

class UserGroup(DeclarativeBase, object):
    """User groups, used eg. to organize users by services, privileges, etc."""

    __tablename__ = bdd_basename + 'usergroup'

    # XXX Faut-il renommer ce champ ?
    group_name = Column(
        Unicode(255),
        primary_key=True)

    permissions = relation('Permission', secondary=USERGROUP_PERMISSION_TABLE,
                      back_populates='usergroups', lazy='dynamic')

    users = relation('User', secondary=USER_GROUP_TABLE,
        back_populates='usergroups')

    def __init__(self, **kwargs):
        super(UserGroup, self).__init__(**kwargs)

    def __unicode__(self):
        return self.group_name

    @classmethod
    def by_group_name(cls, group_name):
        """Return the group object whose group name is ``group_name``."""
        return DBSession.query(cls).filter(cls.group_name == group_name).first()

