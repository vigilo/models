# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2018 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèle pour la table UserGroup"""
from sqlalchemy import Column
from sqlalchemy.types import Unicode, Integer
from sqlalchemy.orm import relation

from vigilo.models.session import DeclarativeBase, DBSession
from vigilo.models.tables.secondary_tables import USERGROUP_PERMISSION_TABLE, \
                                            USER_GROUP_TABLE

__all__ = ('UserGroup', )

class UserGroup(DeclarativeBase, object):
    """
    Gère un groupe d'utilisateurs. Un groupe d'utilisateur peut refléter
    l'organisation d'une entreprise, par exemple avec un découpage en
    "profils" des utilisateurs.

    @ivar idgroup: Identifiant du groupe d'utilisateurs.
    @ivar group_name: Nom du groupe d'utilisateurs.
    @ivar permissions: Liste des L{Permission}s données aux utilisateurs
        du groupe.
    @ivar users: Liste des utilisateurs (L{User}) appartenant au groupe.
    """

    __tablename__ = 'vigilo_usergroup'

    idgroup = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    group_name = Column(
        Unicode(255),
        unique=True,
        index=True,
    )

    permissions = relation('Permission', secondary=USERGROUP_PERMISSION_TABLE,
                      back_populates='usergroups', lazy=True)

    datapermissions = relation('DataPermission', cascade="all",
                      back_populates='usergroup', lazy=True)

    users = relation('User', secondary=USER_GROUP_TABLE,
        back_populates='usergroups', lazy=True)

    def __init__(self, **kwargs):
        """Initialisation dee l'objet."""
        super(UserGroup, self).__init__(**kwargs)

    def __unicode__(self):
        """Représentation unicode."""
        return self.group_name

    @classmethod
    def by_group_name(cls, group_name):
        """
        Renvoie le groupe d'utilisateurs dont le nom est L{group_name}.

        @return: Groupe d'utilisateurs dont le nom est L{group_name}.
        @rtype: L{UserGroup}
        """
        return DBSession.query(cls).filter(cls.group_name == group_name).first()
