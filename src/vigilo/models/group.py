# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Group"""
from sqlalchemy import Column
from sqlalchemy.types import Unicode, Integer
from sqlalchemy.orm import relation, backref
from sqlalchemy.schema import UniqueConstraint

from vigilo.models.configure import DeclarativeBase, DBSession, ForeignKey
from vigilo.models.secondary_tables import GROUP_PERMISSION_TABLE, \
                                            HOST_GROUP_TABLE, \
                                            SERVICE_GROUP_TABLE, \
                                            MAP_GROUP_TABLE, \
                                            GRAPH_GROUP_TABLE#, \
#                                            APPLICATION_GROUP_TABLE, \
#                                            USAGE_TABLE

__all__ = ('HostGroup', 'ServiceGroup', 'MapGroup')

class Group(DeclarativeBase, object):
    """
    Gère des groupes (récursifs).
    Cette classe est abstraite. Utilisez les classes spécialisées
    (L{HostGroup}, L{ServiceGroup}, L{MapGroup}, L{GraphGroup}, etc.)
    pour créer des instances.
    
    @ivar idgroup: Identifiant (auto-généré) du groupe.
    @ivar _grouptype: Discriminant pour savoir le type de groupe manipulé.
        Note: n'utilisez jamais cet attribut dans votre code pour effectuer
        un traitement en fonction du type de groupe. A la place, utilisez
        la fonction isinstance() de Python.
        Exemple: isinstance(grp, HostGroup).
    @ivar name: Nom du groupe, unique pour un type de groupe considéré.
    @ivar idparent: Identifiant du groupe dont le groupe courant est un
        fils. Vaut None si le groupe courant n'a pas de parent.
    @ivar parent: Instance de groupe dont ce groupe hérite.
    @ivar children: Liste des instances de groupes qui héritent du groupe
        courant.
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

    idparent = Column(
        'idparent', Integer,
        ForeignKey(idgroup),
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
    def get_top_groups(cls):
        """
        Renvoie les groupes de premier niveau.
        
        Groupes dont l'attribut parent est nul.

        @param cls: La classe à utiliser, c'est-à-dire L{Group}.
        @type cls: C{class}
        @return: Les groupes de premier niveau.
        @rtype: L{list}
        """
        return DBSession.query(cls).filter(cls.idparent == None).all()


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
    """
    Groupe d'hôtes.

    @ivar permissions: Liste des L{Permission}s qui donnent accès à ce
        groupe d'hôtes.
    @ivar hosts: Liste des L{Host}s appartenant à ce groupe.
    """

    __mapper_args__ = {'polymorphic_identity': u'hostgroup'}

    permissions = relation('Permission', secondary=GROUP_PERMISSION_TABLE,
                    back_populates='hostgroups')

    hosts = relation('Host', secondary=HOST_GROUP_TABLE,
                back_populates='groups')

class ServiceGroup(Group):
    """
    Groupe de services.

    @ivar permissions: Liste des L{Permission}s qui donnent accès à ce
        groupe de services.
    @ivar services: Liste des L{Service}s appartenant à ce groupe.
    """

    __mapper_args__ = {'polymorphic_identity': u'servicegroup'}

    permissions = relation('Permission', secondary=GROUP_PERMISSION_TABLE,
                    back_populates='servicegroups')

    services = relation('Service', secondary=SERVICE_GROUP_TABLE,
                    back_populates='groups')

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

    subgroups = relation('MapGroup', order_by="MapGroup.name")

    maps = relation('Map', secondary=MAP_GROUP_TABLE,
                    back_populates='groups',
                    order_by='Map.title')

class GraphGroup(Group):
    """
    Groupe de graphes.

    @ivar permissions: Liste des L{Permission}s qui donnent accès à ce
        groupe de graphes.
    @ivar graphs: Liste des L{Graph}es appartenant à ce groupe.
    """

    __mapper_args__ = {'polymorphic_identity': u'graphgroup'}

    permissions = relation('Permission', secondary=GROUP_PERMISSION_TABLE,
                    back_populates='graphgroups')

    graphs = relation('Graph', secondary=GRAPH_GROUP_TABLE,
                    back_populates='groups')

