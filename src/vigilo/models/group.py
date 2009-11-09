# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Group"""
from __future__ import absolute_import

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Unicode, Integer
from sqlalchemy.orm import relation, backref

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .session import DBSession
from .secondary_tables import GROUP_PERMISSION_TABLE

__all__ = ('Group', )

class Group(DeclarativeBase, object):
    """Gère les groupes (récursifs) d'hôtes/services.'"""
    __tablename__ = bdd_basename + 'group'

    idgroup = Column(
        Integer,
        primary_key=True, autoincrement=True,
    )

    name = Column(
        Unicode(255),
        unique=True, index=True,
        nullable=False,
    )

    idparent = Column(
        'idparent', Integer,
        ForeignKey(bdd_basename + 'group.idgroup'),
    )

    # XXX We should make sure it's impossible to build cyclic graphs.
    children = relation('Group', backref=backref('parent', remote_side=[idgroup]))

    permissions = relation('Permission', secondary=GROUP_PERMISSION_TABLE,
                    back_populates='groups')

    servicegroups = relation('ServiceGroup',
        back_populates='groups', uselist=True, )

    hostgroups = relation('HostGroup',
        back_populates='groups', uselist=True, )


    def __init__(self, **kwargs):
        """
        Initialise l'instance avec les informations du groupe.
        
        @param kwargs: Un dictionnaire avec les informations sur le groupe.
        @type kwargs: C{dict}
        """
        super(Group, self).__init__(**kwargs)

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

