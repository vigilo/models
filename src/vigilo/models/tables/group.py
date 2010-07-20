# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Group"""
from sqlalchemy import Column
from sqlalchemy.types import Unicode, Integer
from sqlalchemy.orm import relation, aliased, EXT_CONTINUE
from sqlalchemy.orm.interfaces import MapperExtension
from sqlalchemy.sql.expression import exists, not_

from vigilo.models.session import DeclarativeBase, DBSession
from vigilo.models.tables.secondary_tables import MAP_GROUP_TABLE, \
                                                GRAPH_GROUP_TABLE, \
                                                SUPITEM_GROUP_TABLE

__all__ = ('SupItemGroup', 'MapGroup', 'GraphGroup')

class Group(DeclarativeBase, object):
    """
    Gère des groupes.
    Cette classe est abstraite. Utilisez les classes spécialisées
    (L{SupItemGroup}, L{MapGroup}, L{GraphGroup}, etc.) pour créer
    des instances.
    En combinant cette classe à la classe GroupHierarchy, il est possible
    de créer une arborescence de groupes.
    
    @ivar idgroup: Identifiant (auto-généré) du groupe.
    @ivar _grouptype: Discriminant pour savoir le type de groupe manipulé.
        Note: n'utilisez jamais cet attribut dans votre code pour effectuer
        un traitement en fonction du type de groupe. A la place, utilisez
        la fonction isinstance() de Python.
        Exemple : isinstance(grp, HostGroup).
    @ivar name: Nom du groupe.
    """
    __tablename__ = 'group'

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

    __mapper_args__ = {
        'polymorphic_on': _grouptype,
    }

    datapermissions = relation('DataPermission', cascade="all",
                      back_populates='group', lazy=True)

    def __init__(self, **kwargs):
        """
        Initialise l'instance avec les informations du groupe.
        
        @param kwargs: Un dictionnaire avec les informations sur le groupe.
        @type kwargs: C{dict}
        """
        from vigilo.models.tables.grouphierarchy import GroupHierarchy
        loop = GroupHierarchy(parent=self, child=self, hops=0)
        DBSession.add(loop)
        super(Group, self).__init__(**kwargs)

    def __unicode__(self):
        """
        Conversion en unicode.
        
        @return: Le nom du groupe.
        @rtype: C{str}
        """
        return self.name

    def __repr__(self):
        return "<%s \"%s\">" % (self.__class__.__name__, str(self.name))

    # Chemin d'accès

    def get_path(self):
        """
        Renvoie le chemin d'accès jusqu'au groupe.
        
        @return: Chemin d'accès jusqu'à ce groupe.
        @rtype: C{str}
        """
        from .grouphierarchy import GroupHierarchy
        parts = DBSession.query(
                Group.name
            ).join(
                (GroupHierarchy, GroupHierarchy.idparent == Group.idgroup),
            ).filter(GroupHierarchy.idchild == self.idgroup
            ).order_by(GroupHierarchy.hops.desc()
            ).all()
        parts = [p.name.replace('\\', '\\\\').replace('/', '\\/') for p in parts]
        # Force la génération d'un chemin absolu (commençant par '/').
        parts.insert(0, '')
        return '/'.join(parts)

    # Parents

    def has_parent(self):
        from .grouphierarchy import GroupHierarchy
        return (DBSession.query(GroupHierarchy)\
            .filter(GroupHierarchy.idchild == self.idgroup)\
            .filter(GroupHierarchy.hops > 0)\
            .count() > 0)
    
    def get_parent(self):
        from .grouphierarchy import GroupHierarchy
        q = DBSession.query(GroupHierarchy).filter(
                    GroupHierarchy.idchild == self.idgroup
                ).filter(
                    GroupHierarchy.hops == 1
                )
        if q.count() == 0:
            return None
        return q.one().parent
    
    def set_parent(self, group):
        """
        Positionne un groupe en tant que parent du groupe courant.
        Cette méthode ne peut gérer qu'un unique parent, elle ne convient
        donc pas pour les L{SupItemGroup}.

        @param group: Nouveau parent du groupe courant.
        @type group: L{Group}
        @note: Si un groupe était déjà marqué comme parent du groupe courant,
            alors cette association est rompue et une nouvelle hiérarchie
            de groupe est construite pour le nouveau parent.
        """
        from .grouphierarchy import GroupHierarchy

        # On récupère tous nos enfants, petits-enfants, etc..
        children = DBSession.query(GroupHierarchy).filter(
                        GroupHierarchy.parent == self)

        # Supprime tous les liens de parenté du groupe courant
        # et de ses enfants (sans limite de profondeur) vers nos
        # parents (sans limite de profondeur).
        for c in children:
            DBSession.query(GroupHierarchy
                ).filter(GroupHierarchy.idchild == c.idchild
                ).filter(GroupHierarchy.hops > c.hops
                ).delete()

        # Si un groupe doit devenir le nouveau parent.
        if group:
            # Récupère les parents, grands-parents, etc. de notre parent.
            parents = DBSession.query(GroupHierarchy
                ).filter(GroupHierarchy.child == group
                ).all()

            for p in parents:
                # Nos enfants [et petits ...] et nous-même héritons de
                # l'arborescence de nos parents [et grands ...] à une
                # distance augmentée de 1.
                for c in children:
                    GroupHierarchy.get_or_create(
                        idparent=p.idparent,
                        idchild=c.idchild,
                        hops=p.hops + c.hops + 1,
                    )
        DBSession.flush()

    parent = property(get_parent, set_parent)

    def get_top_parent(self):
        """
        Renvoie le parent de plus haut niveau (celui qui n'a pas de parent lui-même)
        @return: Parent de plus haut niveau
        @rtype: L{Group}
        """
        from .grouphierarchy import GroupHierarchy
        top_parent = DBSession.query(Group
            ).join(
                (GroupHierarchy, GroupHierarchy.idparent == Group.idgroup),
            ).filter(GroupHierarchy.idchild == self.idgroup
            ).order_by(GroupHierarchy.hops.desc()
            ).first()
        #if top_parent.has_parent():
        #    # bizarre, on devrait avoir un groupe de plus haut niveau
        #    return None
        return top_parent

    # Fils

    def has_children(self):
        """ renvoie True si le groupe a des enfants
        """
        from .grouphierarchy import GroupHierarchy
        return ( DBSession.query(self.__class__).join(
            (GroupHierarchy, GroupHierarchy.idchild == self.__class__.idgroup),
        ).filter(GroupHierarchy.idparent == self.idgroup
        ).filter(GroupHierarchy.hops == 1
        ).count() > 0)
    
    def get_children(self, hops=1):
        """ renvoie la liste des enfants d'un groupe
        """
        from .grouphierarchy import GroupHierarchy
        children = DBSession.query(self.__class__).join(
                (GroupHierarchy, GroupHierarchy.idchild == \
                    self.__class__.idgroup),
            ).filter(GroupHierarchy.idparent == self.idgroup
            ).order_by(self.__class__.name.asc())

        # Pas de limite sur la distance, on retourne tous les enfants,
        # on exclut juste le nœud courant.
        if not hops:
            children = children.filter(GroupHierarchy.hops > 0)
        else:
            children = children.filter(GroupHierarchy.hops == hops)
        return children.all()

    children = property(get_children)

    def get_all_children(self):
        """ renvoie la liste  des descendants
        """
        from .grouphierarchy import GroupHierarchy
        children = DBSession.query(
                self.__class__
            ).distinct(
            ).join(
                (GroupHierarchy, GroupHierarchy.idchild == self.__class__.idgroup)
            ).filter(GroupHierarchy.idparent == self.idgroup
            ).filter(GroupHierarchy.hops > 0).all()
        return children

    def remove_children(self):
        from .grouphierarchy import GroupHierarchy
        DBSession.query(GroupHierarchy)\
            .filter(GroupHierarchy.idparent == self.idgroup)\
            .delete()

    # Méthodes de classe

    @classmethod
    def get_top_groups(cls):
        """
        Renvoie les groupes de premier niveau.

        @param cls: La classe à utiliser, c'est-à-dire L{Group}.
        @type cls: C{class}
        @return: Les groupes de premier niveau.
        @rtype: L{list}
        """
        from .grouphierarchy import GroupHierarchy

        # On récupère tous les groupes qui ont un parent.
        children = DBSession.query(cls).distinct(
            ).join(
                (GroupHierarchy, GroupHierarchy.idchild == cls.idgroup)
            ).filter(GroupHierarchy.hops > 0)

        # Ensuite on les exclut de la liste des groupes,
        # pour ne garder que ceux qui sont au sommet de l'arbre
        # et qui constituent nos "top groups".
        return DBSession.query(cls).except_(children).order_by(cls.name).all()

    @classmethod
    def by_group_name(cls, groupname):
        """
        Renvoie le groupe dont le nom est C{groupname}.

        @param cls: La classe à utiliser, c'est-à-dire une classe
            qui hérite de L{Group}.
        @type cls: C{class}
        @param groupname: Le nom du groupe que l'on souhaite récupérer.
        @type groupname: C{str}
        @return: Le groupe demandé.
        @rtype: L{Group}
        """
        return DBSession.query(cls).filter(cls.name == groupname).first()

    @classmethod
    def by_parent_and_name(cls, parent, name):
        """
        Renvoie le groupe dont le nom est L{groupname} et qui a L{parent}
        pour parent.

        @param cls: La classe à utiliser, c'est-à-dire une classe
            qui hérite de L{Group}.
        @type cls: C{class}
        @param parent: Instance du parent du groupe demandé ou C{None} pour
            rechercher un groupe au sommet de la hiérarchie.
        @type parent: L{Group} ou C{None}
        @param groupname: Le nom du groupe que l'on souhaite récupérer.
        @type groupname: C{unicode}
        @return: Le groupe demandé.
        @rtype: L{Group} ou C{None}
        """
        from .grouphierarchy import GroupHierarchy

        # Recherche d'un groupe au sommet de la hiérarchie.
        if parent is None:
            cls_alias1 = aliased(cls)
            cls_alias2 = aliased(cls)
            # Retourne le groupe de la classe demandée portant ce nom
            # tel qu'il n'existe pas de groupe qui soit marqué comme
            # étant un parent du groupe retenu.
            return DBSession.query(
                    cls_alias1,
                ).filter(cls_alias1.name == name
                ).filter(
                    not_(exists(
                        ).where(cls_alias1.idgroup == cls_alias2.idgroup
                        ).where(GroupHierarchy.hops > 0
                        ).where(GroupHierarchy.idchild == cls_alias2.idgroup)
                    )
                ).first()

        return DBSession.query(cls
                    ).join(
                        (GroupHierarchy, GroupHierarchy.idchild == cls.idgroup)
                    ).filter(
                        GroupHierarchy.idparent == parent.idgroup
                    ).filter(GroupHierarchy.hops == 1
                    ).filter(cls.name == name).first()


class MapGroup(Group):
    """
    Groupe de cartes.

    @ivar subgroups: Liste des L{MapGroup} qui sont des fils
        du groupe courant.
    @ivar maps: Liste des L{Map}s appartenant à ce groupe.
    """

    __mapper_args__ = {'polymorphic_identity': u'mapgroup'}

    maps = relation('Map', secondary=MAP_GROUP_TABLE,
                    back_populates='groups',
                    order_by='Map.title',
                    cascade="all")

class GraphGroup(Group):
    """
    Groupe de graphes.

    ATTENTION : les groupes de graphes NE SONT PAS récursifs.
    Ils utilisent cependant la même classe de base pour simplifier
    le reste du code (gestion des permissions, etc.).

    @ivar graphs: Liste des L{Graph}es appartenant à ce groupe.
    """

    __mapper_args__ = {'polymorphic_identity': u'graphgroup'}

    graphs = relation('Graph', secondary=GRAPH_GROUP_TABLE,
                    back_populates='groups')

class SupItemGroup(Group):
    """
    Groupe d'éléments supervisés.

    @ivar supitems: Liste des L{SupItem}s appartenant à ce groupe.
    """
    __mapper_args__ = {'polymorphic_identity': u'supitemgroup'}

    supitems = relation('SupItem', secondary=SUPITEM_GROUP_TABLE,
                back_populates='groups')
    
    hosts = relation('Host', secondary=SUPITEM_GROUP_TABLE)
    
    lls = relation('LowLevelService', secondary=SUPITEM_GROUP_TABLE)
    
    hls = relation('HighLevelService', secondary=SUPITEM_GROUP_TABLE)

