# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Permissions"""
from __future__ import absolute_import

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.orm import relation
from pylons.i18n import lazy_ugettext as l_

from .session import DBSession
from .vigilo_bdd_config import bdd_basename, DeclarativeBase, metadata

__all__ = ('Permission', )

USERGROUP_PERMISSION_TABLE = Table(
    bdd_basename + 'usergrouppermissions', metadata,
    Column('groupname', Unicode(255), ForeignKey(
                bdd_basename + 'usergroup.group_name',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
    Column('idpermission', Integer, ForeignKey(
                bdd_basename + 'permission.idpermission',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True)
)

class Permission(DeclarativeBase, object):
    """
    Permission definition for :mod:`repoze.what`.
    Only the ``permission_name`` column is required by :mod:`repoze.what`.
    """

    __tablename__ = bdd_basename + 'permission'

    idpermission = Column(
        Integer,
        autoincrement=True,
        primary_key=True)

    # XXX Faut-il renommer ce champ ?
    permission_name = Column(
        Unicode(255),
        unique=True,
        nullable=False)

    usergroups = relation('UserGroup', secondary=USERGROUP_PERMISSION_TABLE,
                      backref='permissions', lazy='dynamic')

    def __init__(self, **kwargs):
        DeclarativeBase.__init__(self, **kwargs)

    def __unicode__(self):
        return self.permission_name

    @classmethod
    def by_permission_name(cls, perm_name):
        """Return the permission object whose name is ``perm_name``."""
        return DBSession.query(cls).filter(
            cls.permission_name == perm_name).first()


# Rum metadata.
from rum import fields
from .usergroup import UserGroup
from .group import Group

fields.FieldFactory.fields(
    Permission, (
        fields.Unicode('permission_name',
            required=True, searchable=True, sortable=True,
            label=l_('Permission name')),

        fields.Collection('usergroups', UserGroup, 'group_name',
            label=l_('Usergroups')),

        fields.Collection('groups', Group, 'name',
            label=l_('Groups of hosts/services')),
    )
)

