# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2016 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Modèle pour la table maplink et ses tables dérivées par jointure
mapservicelink et mapsegment.
"""
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.orm import relation

from vigilo.models.session import DeclarativeBase, DBSession
from vigilo.models.tables.mapnode import MapNode
from vigilo.models.tables.map import Map
from vigilo.models.tables.graph import Graph
from vigilo.models.tables.service import Service
from vigilo.models.tables.perfdatasource import PerfDataSource

__all__ = ('Link', )

class MapLink(DeclarativeBase, object):
    """
    Informations sur une liaison dans une carte.

    @ivar idmaplink: Identifiant de la liaison.
    @ivar idfrom_node: Identifiant du nœud de départ de la liaison.
    @ivar idto_node: Identifiant du nœud d'arrivée de la liaison.
    @ivar idmap: Référence vers l'identifiant de carte de la liaison.
    @ivar type_link: Type de liaison.
    @ivar from_node: Instance du nœud de départ de la liaison.
    @ivar to_node: Instance du nœud d'arrivée de la liaison.
    """
    __tablename__ = 'vigilo_maplink'

    idmaplink = Column(
        Integer,
        primary_key=True, autoincrement=True, nullable=False,
    )

    idfrom_node = Column(
        Integer,
        ForeignKey(
            MapNode.idmapnode,
            ondelete='CASCADE',
            onupdate='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        nullable=False,
    )

    idto_node = Column(
        Integer,
        ForeignKey(
            MapNode.idmapnode,
            ondelete='CASCADE',
            onupdate='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        nullable=False,
    )

    idmap = Column(
        Integer,
        ForeignKey(
            Map.idmap,
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=True,
            initially='IMMEDIATE',
        ),
        nullable=False,
    )

    type_link = Column(Unicode(16), nullable=False)

    __mapper_args__ = {'polymorphic_on': type_link}

    to_node = relation('MapNode', foreign_keys=[idto_node],
                         primaryjoin='MapLink.idto_node == MapNode.idmapnode',
                         lazy=True)

    from_node = relation('MapNode', foreign_keys=[idfrom_node],
                       primaryjoin='MapLink.idfrom_node == MapNode.idmapnode',
                       lazy=True)

    def __init__(self, **kwargs):
        """Initialise une liaison."""
        super(MapLink, self).__init__(**kwargs)

    def __unicode__(self):
        """
        Formatte un C{MapLink} pour l'afficher dans les formulaires.

        Le nom de la liaison est utilisé pour la représenter dans les formulaires.

        @return: Le nom de la liaison.
        @rtype: C{unicode}
        """
        return self.name

    @classmethod
    def by_link_name(cls, linkname):
        """
        Renvoie la liaison dont le nom est L{linkname}.

        @param linkname: Nom de la liaison voulue.
        @type linkname: C{unicode}
        @return: La liaison demandée.
        @rtype: L{MapLink}
        """
        return DBSession.query(cls).filter(cls.name == linkname).first()


class MapServiceLink(MapLink):
    """
    Classe chargée de la représentation graphique d'une
    liaison de type Service dans VigiMap.

    @ivar idmapservicelink: Identifiant du modèle de l'hôte (séquence).
    @ivar idref: Identifiant du service de bas niveau référencé.
    @ivar reference: Instance du service de bas niveau référencé.
    @ivar idgraph: Identifiant du graphe associé à la liaison.
    @ivar graph: Instance graphe associé à la liaison.
    @ivar map: Relation vers la carte.
    """
    __tablename__ = 'vigilo_mapservicelink'

    idmapservicelink = Column(
        Integer,
        ForeignKey(
            MapLink.idmaplink,
            onupdate='CASCADE',
            ondelete='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
        nullable=False,
    )

    idref = Column(
        Integer,
        ForeignKey(
            Service.idsupitem,
            onupdate='CASCADE',
            ondelete='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        nullable=False,
    )

    reference = relation('Service')

    idgraph = Column(
        Integer,
        ForeignKey(
            Graph.idgraph,
            ondelete='CASCADE',
            onupdate='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
    )

    graph = relation('Graph')

    idds_out = Column(
        Integer,
        ForeignKey(
            PerfDataSource.idperfdatasource,
            ondelete='CASCADE',
            onupdate='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
    )

    idds_in = Column(
        Integer,
        ForeignKey(
            PerfDataSource.idperfdatasource,
            ondelete='CASCADE',
            onupdate='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
    )

    ds_out = relation('PerfDataSource', foreign_keys=[idds_out],
                       primaryjoin='PerfDataSource.idperfdatasource == '
                                    'MapServiceLink.idds_out', lazy=True)

    ds_in = relation('PerfDataSource', foreign_keys=[idds_in],
                       primaryjoin='PerfDataSource.idperfdatasource == '
                                    'MapServiceLink.idds_in', lazy=True)

    map = relation('Map',
        back_populates='links', lazy=True)


    def __init__(self, **kwargs):
        """Initialisation d'une liaison concernant un L{Service}."""
        super(MapServiceLink, self).__init__(**kwargs)


class MapLlsLink(MapServiceLink):
    """
    Classe chargée de la représentation graphique d'une
    liaison de type Service de Bas Niveau dans VigiMap.
    """

    __mapper_args__ = {'polymorphic_identity': u'mapllslink'}


class MapHlsLink(MapServiceLink):
    """
    Classe chargée de la représentation graphique d'une
    liaison de type Service de Bas Niveau dans VigiMap.
    """

    __mapper_args__ = {'polymorphic_identity': u'maphlslink'}


class MapSegment(MapLink):
    """
    Classe chargée de la représentation graphique d'un segment dans VigiMap.

    @ivar idmapsegment: Identifiant du modèle de l'hôte (séquence).
    @ivar color: Couleur du segment.
    @ivar thickness: Épaisseur de trait du segment.
    @ivar map: Instance de la carte.
    """
    __tablename__ = 'vigilo_mapsegment'
    __mapper_args__ = {'polymorphic_identity': u'mapsegment'}

    idmapsegment = Column(
        Integer,
        ForeignKey(
            MapLink.idmaplink,
            onupdate='CASCADE',
            ondelete='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
        nullable=False
    )

    color = Column(
        Unicode(255),
        nullable=False
    )

    thickness = Column(
        Integer,
        nullable=False
    )

    map = relation('Map', back_populates='segments')
