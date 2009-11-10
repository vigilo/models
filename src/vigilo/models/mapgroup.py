# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Group"""
from __future__ import absolute_import

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Unicode, Integer
from sqlalchemy.orm import relation, backref

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .session import DBSession
from .secondary_tables import MAP_GROUP_PERMISSION_TABLE, MAP_GROUP_MAP_TABLE
from .map import Map

__all__ = ('Group', )

class MapGroup(DeclarativeBase, object):
    """
    Gère les groupes (récursifs) de cartes.
    
    @ivar idmapgroup: Identifiant du groupe de cartes.
    @ivar name: Nom du groupe de cartes.
    @ivar parent: Référence vers le groupe de cartes 'parent'.
    @ivar subgroups: Liste des sous-groupes de cartes associées au groupe.
    @ivar permissions: Liste des permissions d'accés au groupe.
    @ivar maps: Liste des cartes associées au groupe.
    """
    __tablename__ = bdd_basename + 'mapgroup'

    idmapgroup = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    
    name = Column(Unicode(255), nullable=False)    

    parent = Column(
        'parent', Integer,
        ForeignKey(bdd_basename + 'mapgroup.idmapgroup'),
        index=True)

    # XXX We should make sure it's impossible to build cyclic graphs.
    subgroups = relation('MapGroup', order_by="MapGroup.name")

    permissions = relation('Permission', secondary=MAP_GROUP_PERMISSION_TABLE,
                            back_populates='mapgroups')

    maps = relation('Map', secondary=MAP_GROUP_MAP_TABLE,
                    back_populates='groups', uselist=True,
                    order_by=Map.title)

    def __init__(self, **kwargs):
        """
        Initialise l'instance avec les informations du groupe de carte.
        
        @param kwargs: Un dictionnaire contenant les informations sur le groupe.
        @type kwargs: C{dict}
        """
        super(MapGroup, self).__init__(**kwargs)

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

