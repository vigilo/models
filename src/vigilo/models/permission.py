# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Permissions"""
from __future__ import absolute_import

from sqlalchemy import Column
from sqlalchemy.types import Integer, Unicode, UnicodeText
from sqlalchemy.orm import relation

from .session import DBSession
from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .secondary_tables import USERGROUP_PERMISSION_TABLE, \
                                GROUP_PERMISSION_TABLE, \
                                MAP_PERMISSION_TABLE

__all__ = ('Permission', )

class Permission(DeclarativeBase, object):
    """
    Permission definition for :mod:`repoze.what`.
    Only the ``permission_name`` column is required by :mod:`repoze.what`.
    """

    __tablename__ = bdd_basename + 'permission'

    idpermission = Column(
        Integer,
        autoincrement=True, primary_key=True, unique=True,
    )

    # XXX Faut-il renommer ce champ ?
    permission_name = Column(
        Unicode(255),
        unique=True, index=True, nullable=False,
    )

    description = Column(
        UnicodeText
    )

    usergroups = relation('UserGroup', secondary=USERGROUP_PERMISSION_TABLE,
                      back_populates='permissions', lazy='dynamic')

    groups = relation('Group', secondary=GROUP_PERMISSION_TABLE,
                    back_populates='permissions')

    maps = relation('Map', secondary=MAP_PERMISSION_TABLE,
                    back_populates='permissions')


    def __init__(self, **kwargs):
        super(Permission, self).__init__(**kwargs)

    def __unicode__(self):
        return self.permission_name

    @classmethod
    def by_permission_name(cls, perm_name):
        """Return the permission object whose name is ``perm_name``."""
        return DBSession.query(cls).filter(
            cls.permission_name == perm_name).first()

