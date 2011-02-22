# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Group"""
from sqlalchemy import Column
from sqlalchemy.types import Unicode, Integer
from sqlalchemy.orm import relation, synonym, reconstructor

from vigilo.models.session import DeclarativeBase, DBSession, ForeignKey
from vigilo.models.tables.secondary_tables import MAP_GROUP_TABLE, \
                                                GRAPH_GROUP_TABLE, \
                                                SUPITEM_GROUP_TABLE
from vigilo.models import nested_sets

__all__ = ('SupItemGroup', 'MapGroup', 'GraphGroup')


class Group(DeclarativeBase, object):
    """
    Gère des groupes.
    Cette classe est abstraite. Utilisez les classes spécialisées
    (L{SupItemGroup}, L{MapGroup}, L{GraphGroup}, etc.) pour créer
    des instances.

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
        primary_key=True,
        autoincrement=True,
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

    _left = Column("tree_left", Integer, nullable=False)
    _right = Column("tree_right", Integer, nullable=False)
    _depth = Column('depth', Integer, nullable=False)
    _path = None
    _parent = None
    _orig_parent = None

    def _get_depth(self):
        return self._depth

    def _get_left(self):
        return self._left

    def _get_right(self):
        return self._right

    def _get_parent(self):
        return self._parent

    def _set_parent(self, parent):
        # On a privé l'instance de son parent.
        # Il n'y a pas vraiment de "bonne solution" ici.
        # On pourrait créer une nouvelle hiérarchie, mais
        # le nommage serait problématique.
        # Autant lever une erreur (l'utilisateur aurait dû
        # déplacer l'instance de l'ancienne hiérarchie vers
        # une nouvelle hiérarchie manuellement).
        if self._orig_parent and not parent:
            raise nested_sets.CannotRemoveParentException()

        if parent:
            # On tente de déplacer le nœud d'une hiérarchie
            # vers une autre. Les modifications seraient
            # trop importantes à gérer, donc on l'empêche.
            # @TODO: autoriser ce genre de déplacements.
            if type(self) != type(parent):
                raise nested_sets.CannotMoveBetweenHierarchiesException()

            # On essaye de déplacer le nœud comme fils de l'un
            # de ses fils actuels (ie. de construire un cycle).
            if self.idgroup and parent.idgroup and \
                parent.left >= self.left and \
                parent.right <= self.right:
                raise nested_sets.CyclicalHierarchyException()

        self._parent = parent
        # Ce changement permet également de marquer l'instance
        # comme ayant été modifiée.
        # Cf. http://groups.google.com/group/sqlalchemy/browse_thread/thread/6c2d90a11783deac/e3e766d915456a6e
        grouptype = self._grouptype
        self._grouptype = grouptype
        self._path = None

    # L'attribut "depth" est mis à jour en fonction du parent,
    # donc l'accès se fait en lecture seule.
    # Idem pour 'left' et 'right'.
    depth = synonym('_depth', descriptor=property(_get_depth))
    left = synonym('_left', descriptor=property(_get_left))
    right = synonym('_right', descriptor=property(_get_right))
    parent = synonym('_parent', descriptor=property(_get_parent, _set_parent))

    __mapper_args__ = {
        'polymorphic_on': _grouptype,
        'extension': nested_sets.NestedSetExtension(),
        'batch': False,
    }

    datapermissions = relation('DataPermission', cascade="all",
                      back_populates='group', lazy=True)

    def __init__(self, **kwargs):
        """
        Initialise l'instance avec les informations du groupe.

        @param kwargs: Un dictionnaire avec les informations sur le groupe.
        @type kwargs: C{dict}
        """
        parent = None
        if 'parent' in kwargs:
            parent = kwargs.pop('parent')
            if parent is None:
                parent = self.by_parent_and_name(None, u'Root')
        elif 'name' not in kwargs or kwargs['name'] != u'Root':
            parent = self.by_parent_and_name(None, u'Root')
        super(Group, self).__init__(parent=parent, **kwargs)

    def __unicode__(self):
        """
        Conversion en unicode.

        @return: Le nom du groupe.
        @rtype: C{unicode}
        """
        return self.name

    def __repr__(self):
        return u"<%s \"%s\">" % (
            self.__class__.__name__,
            unicode(self.name),
        )

    # Chemin d'accès

    def get_path(self):
        """
        Renvoie le chemin d'accès jusqu'au groupe.

        @return: Chemin d'accès jusqu'à ce groupe.
        @rtype: C{str}
        """
        # mise en cache
        path = getattr(self, "_path", None)
        if path:
            return path

        # Cas où on tente de récupérer le chemin du groupe
        # avant que celui-ci n'ait été enregistré dans la base.
        if self._grouptype is None:
            prefix = ''
            if self._parent:
                prefix = self._parent.path
            return prefix + '/' + \
                self.name.replace('\\', '\\\\').replace('/', '\\/')

        parts = DBSession.query(
                self.__class__.name,
            ).filter(self.__class__.left <= self.left
            ).filter(self.__class__.right >= self.right
            ).order_by(self.__class__.depth.asc()
            ).all()

        parts = [
                    p.name.replace('\\', '\\\\').replace('/', '\\/')
                    for p in parts
                ]
        self._path = '/' + '/'.join(parts)
        return self._path
    path = property(get_path)

    # Parents

    def has_parent(self):
        """
        Renvoie True si ce groupe a un parent.
        """
        return bool(self.parent)

    def get_top_parent(self):
        """
        Renvoie le parent de plus haut niveau
        (celui qui n'a pas de parent lui-même)
        dans la hiérarchie de ce groupe.
        @return: Parent de plus haut niveau
            dans cette hiérarchie.
        @rtype: L{Group}
        """
        return DBSession.query(
                self.__class__
            ).filter(self.__class__._grouptype == self._grouptype
            ).filter(self.__class__.depth == 0
            ).one()


    # Fils

    def has_children(self):
        """
        Renvoie True si le groupe a des enfants.
        """
        return (self.right != self.left + 1)

    def get_children(self, hops=1):
        """
        Renvoie la liste des enfants du groupe.
        """
        children = DBSession.query(
                self.__class__
            ).filter(self.__class__._grouptype == self._grouptype
            ).filter(self.__class__.left.between(self.left, self.right)
            ).order_by(self.__class__.name.asc())

        if hops:
            children = children.filter(
                self.__class__.depth == self.depth + hops)
        return children.all()

    children = property(get_children)

    def get_all_children(self):
        """
        Renvoie la liste des descendants du groupe, c'est-à-dire
        la liste de ses fils, petit-fils, etc.
        """
        return DBSession.query(
                self.__class__
            ).filter(self.__class__._grouptype == self._grouptype
            ).filter(self.__class__.left.between(self.left, self.right)
            ).all()

    def remove_children(self):
        """
        Supprime la relation de descendance entre ce groupe
        et tous ses descendants.
        """
        left = self.left
        right = self.right
        width = right - left - 1
        DBSession.query(
                Group
            ).filter(Group._grouptype == self._grouptype
            ).filter(Group.left.between(left, right)
            ).delete()
        DBSession.query(
                Group
            ).filter(Group._grouptype == self._grouptype
            ).filter(Group.right >= right
            ).update({'tree_right': Group.right - width})
        DBSession.query(
                Group
            ).filter(Group._grouptype == self._grouptype
            ).filter(Group.left >= right
            ).update({'tree_left': Group.left - width})
        self._right = self._left + 1


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
        return DBSession.query(cls).filter(cls.depth == 0
            ).order_by(cls.name.asc()).all()

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
        @obsolete: Le groupe retourné par cette méthode n'est pas
            toujours celui escompté (si plusieurs groupes dans la
            même hiérarchie ont le même nom). Utilisez la méthode
            by_parent_and_name() à la place dans le nouveau code.
        """
        return DBSession.query(cls).filter(cls.name == groupname).first()

    @classmethod
    def by_parent_and_name(cls, parent, name):
        """
        Renvoie le groupe dont le nom est L{name} et qui a L{parent}
        pour parent.

        @param cls: La classe à utiliser, c'est-à-dire une classe
            qui hérite de L{Group}.
        @type cls: C{class}
        @param parent: Instance du parent du groupe demandé ou C{None} pour
            rechercher un groupe au sommet de la hiérarchie.
        @type parent: L{Group} ou C{None}
        @param name: Le nom du groupe que l'on souhaite récupérer.
        @type name: C{unicode}
        @return: Le groupe demandé.
        @rtype: L{Group} ou C{None}
        """
        # Recherche d'un groupe au sommet de la hiérarchie.
        if parent is None:
            return DBSession.query(
                    cls
                ).filter(cls.depth == 0
                ).filter(cls.name == unicode(name)
                ).first()

        if parent.depth is None:
            DBSession.add(parent)
            DBSession.flush()

        return DBSession.query(
                cls
            ).filter(cls._grouptype == parent._grouptype
            ).filter(cls.left.between(parent.left, parent.right)
            ).filter(cls.name == unicode(name)
            ).filter(cls.depth == parent.depth + 1
            ).first()


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
                    cascade="all",
                    lazy=True)

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
                    back_populates='groups', lazy=True)

class SupItemGroup(Group):
    """
    Groupe d'éléments supervisés.

    @ivar supitems: Liste des L{SupItem}s appartenant à ce groupe.
    """
    __mapper_args__ = {'polymorphic_identity': u'supitemgroup'}

    supitems = relation('SupItem', secondary=SUPITEM_GROUP_TABLE,
                back_populates='groups', lazy=True)

    hosts = relation('Host', secondary=SUPITEM_GROUP_TABLE, lazy=True)

    lls = relation('LowLevelService', secondary=SUPITEM_GROUP_TABLE, lazy=True)

    hls = relation('HighLevelService', secondary=SUPITEM_GROUP_TABLE, lazy=True)

    def get_ventilation_candidate(self):
        group = self
        while group:
            if group.depth == 1:
                return group
            group = group.parent
        return None

#        return DBSession.query(
#                self.__class__
#            ).filter(self.__class__.depth == 1
#            ).filter(self.__class__.left <= self.left
#            ).filter(self.__class__.right >= self.right
#            ).one()
