# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Group"""
from __future__ import absolute_import

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Unicode, Integer
from sqlalchemy.orm import relation, backref
from sqlalchemy.schema import UniqueConstraint

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .session import DBSession
from .secondary_tables import GROUP_PERMISSION_TABLE, \
                                HOST_GROUP_TABLE, \
                                SERVICE_GROUP_TABLE, \
                                MAP_GROUP_TABLE

__all__ = ('HostGroup', 'ServiceGroup', 'MapGroup')

class Group(DeclarativeBase, object):
    """Gère les groupes (récursifs) d'hôtes/services.'"""
    __tablename__ = bdd_basename + 'group'
    __table_args__ = (
        UniqueConstraint('grouptype', 'name'),
        {}
    )

    idgroup = Column(
        Integer,
        primary_key=True, autoincrement=True,
    )

    _grouptype = Column(
        'grouptype', Unicode(20),
        index=True, nullable=False,
    )

    name = Column(
        Unicode(255),
        index=True,
        nullable=False,
    )

    idparent = Column(
        'idparent', Integer,
        ForeignKey(bdd_basename + 'group.idgroup'),
    )

    # XXX We should make sure it's impossible to build cyclic graphs.
    children = relation('Group', backref=backref('parent',
                    remote_side=[idgroup]))

    __mapper_args__ = {'polymorphic_on': _grouptype}

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


class HostGroup(Group):
    __mapper_args__ = {'polymorphic_identity': u'hostgroup'}

    permissions = relation('Permission', secondary=GROUP_PERMISSION_TABLE,
                    back_populates='hostgroups')

    hosts = relation('Host', secondary=HOST_GROUP_TABLE,
                back_populates='groups')

class ServiceGroup(Group):
    __mapper_args__ = {'polymorphic_identity': u'servicegroup'}

    permissions = relation('Permission', secondary=GROUP_PERMISSION_TABLE,
                    back_populates='servicegroups')

    services = relation('ServiceLowLevel', secondary=SERVICE_GROUP_TABLE,
                    back_populates='groups')

class MapGroup(Group):
    __mapper_args__ = {'polymorphic_identity': u'mapgroup'}

    permissions = relation('Permission', secondary=GROUP_PERMISSION_TABLE,
                    back_populates='mapgroups')

    subgroups = relation('MapGroup', order_by="MapGroup.name")

    maps = relation('Map', secondary=MAP_GROUP_TABLE,
                    back_populates='groups',
                    order_by='Map.title')

