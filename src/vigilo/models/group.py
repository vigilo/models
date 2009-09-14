# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Group"""
from __future__ import absolute_import

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.types import UnicodeText, Integer
from sqlalchemy.orm import relation, backref
from .session import DBSession

from .vigilo_bdd_config import bdd_basename, DeclarativeBase, metadata

GROUP_PERMISSION_TABLE = Table(
    bdd_basename + 'grouppermissions', metadata,
    Column('groupname', UnicodeText, ForeignKey(
                bdd_basename + 'group.name',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
    Column('idpermission', Integer, ForeignKey(
                bdd_basename + 'permission.idpermission',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False)
)

class Group(DeclarativeBase, object):
    """Gère les groupes (récursifs) d'hôtes/services.'"""
    __tablename__ = bdd_basename + 'group'

    name = Column(
        UnicodeText(),
        primary_key=True, nullable=False,
        info={'rum': {'field': 'Text'}})

    _parent = Column(
        'parent', UnicodeText(),
        ForeignKey(bdd_basename + 'group.name'),
        index=True,
        info={'rum': {'field': 'Text'}})

    children = relation('Group', backref=backref('parent', remote_side=[name]))

    permissions = relation('Permission', secondary=GROUP_PERMISSION_TABLE,
                    backref='groups')


    def __init__(self, **kwargs):
        """
        Initialise l'instance avec les informations du groupe.
        
        @param kwargs: Un dictionnaire contenant les informations sur le groupe.
        @type kwargs: C{dict}
        """
        DeclarativeBase.__init__(self, **kwargs)

    def __unicode__(self):
        """
        Conversion en unicode.
        
        @return: Le nom du groupe.
        @rtype: C{str}
        """
        return self.name


    @classmethod
    def by_group_name(cls, groupname):
        """
        Renvoie le groupe dont le nom est C{groupname}.

        @param cls: La classe à utiliser, c'est-à-dire L{Group}.
        @type cls: C{class}
        @param groupname: Le nom du groupe que l'on souhaite récupérer.
        @type groupname: C{str}
        @return: Le groupe demandé.
        @rtype: Une instance de la classe L{Group}
        """
        return DBSession.query(cls).filter(cls.name == groupname).first()

