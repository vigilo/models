# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2011 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèle pour la table Map"""
from sqlalchemy import Column
from sqlalchemy.types import Unicode, DateTime, Integer, Boolean
from sqlalchemy.orm import relation, aliased

from vigilo.models.session import DeclarativeBase, DBSession
from vigilo.models.tables.secondary_tables import MAP_GROUP_TABLE, \
                                                SUB_MAP_NODE_MAP_TABLE
#from vigilo.models.tables.group import MapGroup

__all__ = ('Map', )

class Map(DeclarativeBase, object):
    """
    Informations sur une carte.
    @ivar idmap: Identifiant de la carte.
    @ivar mtime: Date de dernière modification de la carte.
    @ivar title: Titre de la carte.
    @ivar background_color: Couleur d'arrière-plan (propriété CSS).
    @ivar background_image: Image d'arrière-plan (propriété CSS).
    @ivar background_position: Position d'arrière-plan (propriété CSS).
    @ivar background_repeat: Répétition d'arrière-plan (propriété CSS).
    @ivar groups: Liste des L{MapGroup}s auxquels cette carte appartient.
    @ivar links: Liste des liaisons (L{MapServiceLink}) présentes sur la carte.
    @ivar nodes: Liste des nœuds (L{MapNode}) présents sur la carte.
    @ivar segments: Liste des segments (L{MapSegment}) présents sur la carte.
    """
    __tablename__ = 'map'

    idmap = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )

    mtime = Column(DateTime(timezone=False))

    title = Column(Unicode(255), nullable=False)

    background_color = Column(Unicode(8))
    background_image = Column(Unicode(255))
    background_position = Column(Unicode(255))
    background_repeat = Column(Unicode(255))
    generated =  Column(
        Boolean,
        default = False,
        nullable = False)

    groups = relation('MapGroup', secondary=MAP_GROUP_TABLE,
                         back_populates='maps', lazy=True)

    links = relation('MapServiceLink', back_populates='map',
                     lazy=True, cascade="all")

    nodes = relation('MapNode', back_populates='map',
                     lazy=True, cascade="all",
                     order_by='MapNode.label')

    segments = relation('MapSegment', back_populates='map',
                        lazy=True, cascade="all")


    def __init__(self, **kwargs):
        """Initialise une carte."""
        super(Map, self).__init__(**kwargs)

    def __unicode__(self):
        """
        Formatte un C{Map} pour l'afficher dans les formulaires.

        Le titre de la carte est utilisé pour représenter la carte
        dans les formulaires.

        @return: Le titre de la carte.
        @rtype: C{unicode}
        """
        return self.title

    @classmethod
    def by_group_and_title(cls, group, maptitle):
        """
        Renvoie la carte dont le titre est L{maptitle} et qui appartient
        au groupe L{group}.

        @param group: Nom, identifiant ou instance du groupe.
        @type group: C{unicode} ou C{int} ou C{MapGroup}
        @param maptitle: Titre de la carte voulue.
        @type maptitle: C{unicode}
        @return: L'instance correspondant à la carte demandée.
        @rtype: L{Map}
        @note: En pratique, le couple groupe/titre n'est pas unique,
            mais l'utilisateur n'a aucun intérêt à avoir deux cartes
            portant le même titre dans le même groupe, donc on devrait
            être assez tranquilles.
        """
        return DBSession.query(cls
            ).join(
                (MAP_GROUP_TABLE, MAP_GROUP_TABLE.c.idmap == cls.idmap),
            ).filter(cls.title == maptitle
            ).filter(MAP_GROUP_TABLE.c.idgroup == group.idgroup
            ).first()

    @classmethod
    def has_submaps(cls, idmap):
        """
        Indique si une carte possède des sous-cartes ou non.

        @param cls: Classe à utiliser pour le test.
        @type cls: L{Map}
        @param idmap: Identifiant de la carte pour laquelle
            le test doit avoir lieu.
        @type idmap: C{int}
        @return: Drapeau indiquant si la carte a des sous-cartes.
        @rtype: C{bool}
        """
        from .mapnode import MapNode
        map_alias = aliased(Map)
        return (DBSession.query(
                    map_alias
                ).join(
                    (SUB_MAP_NODE_MAP_TABLE, SUB_MAP_NODE_MAP_TABLE.c.idmap == \
                        map_alias.idmap),
                    (MapNode, MapNode.idmapnode == \
                        SUB_MAP_NODE_MAP_TABLE.c.mapnodeid),
                    (cls, cls.idmap == MapNode.idmap),
                ).filter(cls.idmap == idmap
                ).count() > 0)

    @classmethod
    def get_submaps(cls, idmap):
        """
        Renvoie l'ensemble des instances de sous-cartes d'une carte.

        @param cls: Classe à utiliser pour l'obtention des sous-cartes.
        @type cls: L{Map}
        @param idmap: Identifiant de la carte dont les sous-cartes
            doivent être retournées.
        @type idmap: C{int}
        @return: Sous-cartes de la carte identifiée par L{idmap}.
        @rtype: C{list} of L{Map}
        """
        from .mapnode import MapNode
        map_alias = aliased(Map)
        return (DBSession.query(map_alias) \
            .join((SUB_MAP_NODE_MAP_TABLE,
                   SUB_MAP_NODE_MAP_TABLE.c.idmap == map_alias.idmap)) \
            .join((MapNode,
                   MapNode.idmapnode == SUB_MAP_NODE_MAP_TABLE.c.mapnodeid)) \
            .join((cls, cls.idmap == MapNode.idmap)) \
            .filter(cls.idmap == idmap).distinct().order_by(Map.title).all())
