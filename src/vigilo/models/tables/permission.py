# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2016 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèle pour la table Permissions"""
from sqlalchemy import Column
from sqlalchemy.types import Integer, Unicode, UnicodeText
from sqlalchemy.orm import relation

from vigilo.models.session import DeclarativeBase, DBSession
from vigilo.models.tables.secondary_tables import USERGROUP_PERMISSION_TABLE

__all__ = ('Permission', )

class Permission(DeclarativeBase, object):
    """
    Cette classe définit une permission.

    @ivar idpermission: Identifiant (autogénéré) de la permission.
    @ivar permission_name: Nom de la permission (ex: "manage").
    @ivar description: Description intelligible du rôle de la permission.
    @ivar usergroups: Liste des groupes d'utilisateurs possédant
        cette permission.
    @ivar hostgroups: Liste des groupes d'hôtes accessibles grâce à
        cette permission.
    @ivar servicegroups: Liste des groupes de services accessibles grâce à
        cette permission.
    @ivar mapgroups: Liste des groupes de cartes accessibles grâce à
        cette permission.
    @ivar graphgroups: Liste des groupes de graphes accessibles grâce à
        cette permission.
    @ivar maps: Liste des cartes accessibles grâce à cette permission.
    """

    __tablename__ = 'vigilo_permission'

    idpermission = Column(
        Integer,
        autoincrement=True, primary_key=True, unique=True,
    )

    permission_name = Column(
        Unicode(255),
        unique=True, index=True, nullable=False,
    )

    description = Column(
        UnicodeText
    )

    usergroups = relation('UserGroup', secondary=USERGROUP_PERMISSION_TABLE,
                      back_populates='permissions', lazy=True)

    def __init__(self, **kwargs):
        """Initialisation des informations concernant la permission."""
        super(Permission, self).__init__(**kwargs)

    def __unicode__(self):
        """Représentation unicode de la permission."""
        return self.permission_name

    @classmethod
    def by_permission_name(cls, perm_name):
        """Return the permission object whose name is ``perm_name``."""
        return DBSession.query(cls).filter(
            cls.permission_name == perm_name).first()

