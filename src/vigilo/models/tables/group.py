# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Group"""
from sqlalchemy import Column
from sqlalchemy.types import Unicode, Integer
from sqlalchemy.orm import relation, backref
from sqlalchemy.schema import UniqueConstraint

from vigilo.models.session import DeclarativeBase, DBSession, ForeignKey
from vigilo.models.tables.secondary_tables import GROUP_PERMISSION_TABLE, \
                                                MAP_GROUP_TABLE, \
                                                GRAPH_GROUP_TABLE, \
                                                SUPITEM_GROUP_TABLE#, \
#                                                APPLICATION_GROUP_TABLE, \
#                                                USAGE_TABLE

__all__ = ('SupItemGroup', 'MapGroup')

class Group(DeclarativeBase, object):
    """
    Gère des groupes.
    Cette classe est abstraite. Utilisez les classes spécialisées
    (L{HostGroup}, L{ServiceGroup}, L{MapGroup}, L{GraphGroup}, etc.)
    pour créer des instances.
    En combinant cette classe à la classe GroupHierarchy, il est possible
    de créer une arborescence de groupes.
    
    @ivar idgroup: Identifiant (auto-généré) du groupe.
    @ivar _grouptype: Discriminant pour savoir le type de groupe manipulé.
        Note: n'utilisez jamais cet attribut dans votre code pour effectuer
        un traitement en fonction du type de groupe. A la place, utilisez
        la fonction isinstance() de Python.
        Exemple: isinstance(grp, HostGroup).
    @ivar name: Nom du groupe, unique pour un type de groupe considéré.
    """
    __tablename__ = 'group'
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
    
    def remove_children(self):
        """
        """
        from .grouphierarchy import GroupHierarchy
        DBSession.query(GroupHierarchy)\
            .filter(GroupHierarchy.idparent == self.idgroup)\
            .delete()
    
    def has_parent(self):
        from .grouphierarchy import GroupHierarchy
        return (DBSession.query(GroupHierarchy)\
            .filter(GroupHierarchy.idchild == self.idgroup)\
            .filter(GroupHierarchy.hops > 0)\
            .count() > 0)
    
    def get_parent(self):
        from .grouphierarchy import GroupHierarchy
        q = DBSession.query(GroupHierarchy)\
            .filter(GroupHierarchy.idchild == self.idgroup)
        if q.count() == 0:
            return None
        return q.one().parent
    
    def set_parent(self, group):
        """ positionne un groupe en tant que parent
        """
        from .grouphierarchy import GroupHierarchy
        # on détruit un éventuel lien de parenté existant
        DBSession.query(GroupHierarchy
                            ).filter(GroupHierarchy.idchild == self.idgroup
                            ).filter(GroupHierarchy.idparent == group.idgroup
                            ).delete()
        gh = GroupHierarchy(parent=group, child=self, hops=1)
        DBSession.add(gh)
    
    @classmethod
    def create(cls, name, parent=None, flush=True):
        """ méthode de création d'un groupe.
        
        TODO: construire les liens hops > 1
        
        @param name: nom du groupe
        @type nom: C{str}
        @param parent: groupe parent
        @type parent: C{Group}
        @param flush: invoque l'appel au flush db
        @type flush: C{Boolean}
        """
        from .grouphierarchy import GroupHierarchy
        group = cls(name=name)
        DBSession.add(group)
    
        DBSession.add(GroupHierarchy(
            parent=group,
            child=group,
            hops=0,
        ))
        if parent:
            DBSession.add(GroupHierarchy(
                parent=parent,
                child=group,
                hops=1,
            ))
            
        if flush:
            DBSession.flush()
        return group
    
    def get_all_children(self):
        """ renvoie la liste  des descendants
        """
        from .grouphierarchy import GroupHierarchy
        children = DBSession.query(
                self.__class__
            ).distinct(
            ).join(
                (GroupHierarchy, GroupHierarchy.idchild == self.__class__.idgroup)
            ).filter(GroupHierarchy.hops > 0)
        return children
    
    """ TODO:
        topgroups = DBSession.query(
                SupItemGroup,
            ).filter(SupItemGroup.idgroup.in_(supitemgroups)
            ).except_(children).order_by(SupItemGroup.name).all()
        topgroups = [(sig.name, str(sig.idgroup)) for sig in topgroups]
    """

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

class MapGroup(Group):
    """
    Groupe de cartes.

    @ivar permissions: Liste des L{Permission}s qui donnent accès à ce
        groupe de cartes.
    @ivar subgroups: Liste des L{MapGroup} qui sont des fils
        du groupe courant.
    @ivar maps: Liste des L{Map}s appartenant à ce groupe.
    """

    __mapper_args__ = {'polymorphic_identity': u'mapgroup'}

    permissions = relation('Permission', secondary=GROUP_PERMISSION_TABLE,
                    back_populates='mapgroups')

    @property
    def subgroups(self):
        from .grouphierarchy import GroupHierarchy
        return DBSession.query(MapGroup).join(
            (GroupHierarchy, GroupHierarchy.idchild == MapGroup.idgroup),
        ).filter(GroupHierarchy.idparent == self.idgroup
        ).filter(GroupHierarchy.hops == 1
        ).order_by(MapGroup.name.asc()
        ).all()

    maps = relation('Map', secondary=MAP_GROUP_TABLE,
                    back_populates='groups',
                    order_by='Map.title')

class GraphGroup(Group):
    """
    Groupe de graphes.

    ATTENTION : les groupes de graphes NE SONT PAS récursifs.
    Ils utilisent cependant la même classe de base pour simplifier
    le reste du code (gestion des permissions, etc.).

    @ivar permissions: Liste des L{Permission}s qui donnent accès à ce
        groupe de graphes.
    @ivar graphs: Liste des L{Graph}es appartenant à ce groupe.
    """

    __mapper_args__ = {'polymorphic_identity': u'graphgroup'}

    graphs = relation('Graph', secondary=GRAPH_GROUP_TABLE,
                    back_populates='groups')

class SupItemGroup(Group):
    """
    Groupe d'éléments supervisés.

    @ivar permissions: Liste des L{Permission}s qui donnent accès à ce
        groupe d'éléments supervisés.
    @ivar supitems: Liste des L{SupItem}s appartenant à ce groupe.
    """
    __mapper_args__ = {'polymorphic_identity': u'supitemgroup'}

    permissions = relation('Permission', secondary=GROUP_PERMISSION_TABLE,
                    back_populates='supitemgroups')

    supitems = relation('SupItem', secondary=SUPITEM_GROUP_TABLE,
                back_populates='groups')
    
    def has_children(self):
        """ renvoie True si le groupe a des enfants
        """
        from .grouphierarchy import GroupHierarchy
        return ( DBSession.query(SupItemGroup).join(
            (GroupHierarchy, GroupHierarchy.idchild == SupItemGroup.idgroup),
        ).filter(GroupHierarchy.idparent == self.idgroup
        ).count() > 0 )
    
    def get_children(self, hops=1):
        """ renvoie la liste des enfants d'un groupe
        """
        from .grouphierarchy import GroupHierarchy
        return DBSession.query(SupItemGroup).join(
            (GroupHierarchy, GroupHierarchy.idchild == SupItemGroup.idgroup),
        ).filter(GroupHierarchy.idparent == self.idgroup
        ).filter(GroupHierarchy.hops == 1
        ).all()
    
    def get_hosts(self):
        """ renvoie les hôtes appartenant au groupe
        """
        from vigilo.models.tables import Host
        hosts = []
        for si in self.supitems:
            if si.__class__ == Host:
                hosts.append(si)
        return hosts
    
    def get_services(self, level='all'):
        """ renvoie les services appartenant au groupe
        level = all | low | high
        """
        from vigilo.models.tables import LowLevelService, HighLevelService
        services = []
        for si in self.supitems:
            if si.__class__ == LowLevelService:
                if level in ('all', 'low'):
                    services.append(si)
            elif si.__class__ == HighLevelService:
                if level in ('all', 'high'):
                    services.append(si)
        return services
    
    """ TODO:
        hostgroups = DBSession.query(
                SupItemGroup.name,
                SupItemGroup.idgroup,
            ).distinct().join(
                (GroupHierarchy, GroupHierarchy.idchild == \
                    SupItemGroup.idgroup),
            ).filter(GroupHierarchy.idparent == maingroupid
            ).filter(GroupHierarchy.hops == 1
            ).filter(SupItemGroup.idgroup.in_(supitemgroups)
            ).order_by(
                SupItemGroup.name.asc(),
            ).all()
        hostgroups = [(hg.name, str(hg.idgroup)) for hg in hostgroups]
    """