# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2016 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Modèle pour la table MapNode
"""
from sqlalchemy import Column
from sqlalchemy.types import Integer, Unicode, Boolean, Enum
from sqlalchemy.orm import relation

from vigilo.models.session import DeclarativeBase, ForeignKey, DBSession
from vigilo.models.tables.secondary_tables import SUB_MAP_NODE_MAP_TABLE
from vigilo.models.tables.map import Map
from vigilo.models.tables.host import Host
from vigilo.models.tables.service import Service

__all__ = ('MapNodeHost', 'MapNodeService', 'MapNodeLls', 'MapNodeHls',
           'MapNodePerformance')


class MapNode(DeclarativeBase, object):
    """
    Classe abstraite pour représenter un nœud présent sur une carte
    affichée dans VigiMap. Les classes L{MapNodeHost}, L{MapNodeService}, etc.
    correspondent aux classes concrètes utilisées pour la représentation
    des cartes.

    @ivar idmapnode: Identifiant du modèle de nœud (séquence).
    @ivar label: Label du nœud.
    @ivar x_pos: Abscisse du nœud.
    @ivar y_pos: Ordonnée du nœud.
    @ivar minimize: Booléen indiquant l'action à effectuer.
    @ivar type_node: Le type de nœud, peut etre
        'host', 'service',  ou 'performance'.
    @ivar idmap: Référence vers un identifiant de carte.
    @ivar icon: Nom de l'icône du noeud.
    @ivar map: Relation vers la carte du nœud.
    @ivar submaps: Liste des sous-cartes associées au nœud.
    """
    __tablename__ = 'mapnode'

    idmapnode = Column(
        Integer,
        primary_key=True, autoincrement=True, nullable=False,
    )

    label = Column(Unicode(255))

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

    x_pos = Column(Integer, nullable=True)

    y_pos = Column(Integer, nullable=True)

    minimize = Column(
        Boolean,
        default = False,
        nullable = False)

    widget = Column(Unicode(32), nullable=False, default=u"SimpleElement")

    map = relation('Map', back_populates='nodes')

    submaps = relation('Map', secondary=SUB_MAP_NODE_MAP_TABLE)

    # Il est possible de créer des éléments sur la carte
    # qui n'ont pas de relations avec les SupItem, mais
    # permettent juste d'ajouter un label, une image et
    # éventuellement des liens vers des sous-cartes.
    type_node = Column(Unicode(16), nullable=True)

    icon = Column(
        Unicode(255)
        )

    links_from = relation('MapLink', foreign_keys=[idmapnode],
                    primaryjoin='MapLink.idfrom_node == '
                        'MapNode.idmapnode')

    links_to = relation('MapLink', foreign_keys=[idmapnode],
                    primaryjoin='MapLink.idto_node == '
                        'MapNode.idmapnode')

    __mapper_args__ = {'polymorphic_on': type_node}


    def __init__(self, **kwargs):
        """Initialise un noeud."""
        super(MapNode, self).__init__(**kwargs)

    def __unicode__(self):
        """
        Formatte un C{Node} pour l'afficher dans les formulaires.

        Le nom du noeud est utilisé pour le représenter dans les formulaires.

        @return: Le nom du node.
        @rtype: C{str}
        """
        return self.idmapnode

    def __repr__(self):
        return "<%s %d>" % (self.__class__.__name__, self.idmapnode)

    @classmethod
    def by_map_label(cls, idmap, label):
        """
        Retourne un élément de la carte dont le libellé correspond
        à celui donné.

        @param cls: La classe de l'instance à retourner (ex: L{MapNode}).
        @type cls: C{type}
        @param idmap: Identifiant de la carte sur lequel l'élément apparaît.
        @type idmap: C{int}
        @param label: Libellé de l'élément sur la carte.
        @type label: C{unicode}
        @return: Instance de la classe correspondant à l'élément demandé.
        @rtype: C{cls}
        @note: Le libellé des éléments n'est pas unique sur une carte.
            Cette fonction ne retourne que le premier élément trouvé en
            base de données. Mieux vaut donc l'utiliser avec précautions.
        """
        if not isinstance(idmap, int):
            idmap = idmap.idmap
        return DBSession.query(cls).filter(
                    cls.idmap == idmap
                ).filter(
                    cls.label == label
                ).first()


class MapNodeHost(MapNode):
    """
    Classe chargée de la représentation graphique d'un hôte dans vigimap

    @ivar idmapnode: Identifiant du modèle de l'hôte (séquence).
    @ivar idhost: Identifiant de l'L{Host} représenté.
    @ivar host: Instance de l'L{Host} représenté.
    """
    __tablename__ = 'mapnodehost'
    __mapper_args__ = {'polymorphic_identity': u'host'}

    idmapnode = Column(
        Integer,
        ForeignKey(
            MapNode.idmapnode,
            onupdate='CASCADE',
            ondelete='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        autoincrement=True,
        primary_key=True,
        nullable=False,
    )

    idhost = Column(
        Integer,
        ForeignKey(
            Host.idhost,
            onupdate='CASCADE',
            ondelete='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        nullable=False,
    )

    host = relation('Host', lazy=True)


    def __init__(self, **kwargs):
        super(MapNodeHost, self).__init__(**kwargs)

    def __unicode__(self):
        """
        Formatte un C{MapNode} pour l'afficher dans les formulaires.
        @return: Le nom du node.
        @rtype: C{str}
        """
        return "%(hostname)s [#%(idmapnode)d]" % {
            'idmapnode': self.idmapnode,
            'hostname':  self.host.name,
        }


class MapNodeService(MapNode):
    """
    Classe chargée de la représentation graphique d'un service dans VigiMap.

    @ivar idmapnode: Identifiant du modèle de service (séquence).
    @ivar idservice: Identifiant du L{Service} représenté.
    @ivar service: Instance du L{Service} représenté.
    @ivar show_deps: Contrôle l'affichage des dépendances pour les services
        de haut niveau.
     """
    __tablename__ = 'mapnodeservice'

    show_deps_flags = {
        'never': 0,
        'problems': 1,
        'always': 2,
    }

    idmapnode = Column(
        Integer,
        ForeignKey(
            MapNode.idmapnode,
            onupdate='CASCADE',
            ondelete='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        autoincrement=False,
        primary_key=True,
        nullable=False
    )

    idservice = Column(
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

    service = relation('Service')

    show_deps = Column(
        Enum(
            # Ne jamais afficher les états des dépendances du HLS.
            'never',

            # N'afficher que les dépendances dans un état anormal.
            'problems',

            # Toujours afficher l'état de l'ensemble des dépendances.
            'always',

            name='vigilo_mapnodehls_show_deps',
        ),
        nullable=False,
        default='never',
    )


    def __init__(self, **kwargs):
        super(MapNodeService, self).__init__(**kwargs)

    def __unicode__(self):
        """
        Formatte un C{MapNode} pour l'afficher dans les formulaires.
        @return: Le nom du node.
        @rtype: C{str}
        """
        return "%(servicename)s [#%(idmapnode)d]" % {
            'idmapnode': self.idmapnode,
            'servicename':  self.service.servicename,
        }


class MapNodeLls(MapNodeService):
    """
    Classe chargée de la représentation graphique d'un service de bas niveau
    dans VigiMap.

    """
    __mapper_args__ = {'polymorphic_identity': u'lls'}



class MapNodeHls(MapNodeService):
    """
    Classe chargée de la représentation graphique d'un service de haut niveau
    dans VigiMap.

    """
    __mapper_args__ = {'polymorphic_identity': u'hls'}
