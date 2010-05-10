# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table User"""
from sqlalchemy.orm import synonym, relation
from sqlalchemy import Column, and_
from sqlalchemy.types import Unicode, DateTime
import hashlib

from vigilo.models.session import DeclarativeBase, DBSession
from vigilo.models.tables.secondary_tables import USER_GROUP_TABLE, \
                                            GROUP_PERMISSION_TABLE, \
                                            USERGROUP_PERMISSION_TABLE
from vigilo.models.tables import SupItemGroup, MapGroup, \
                                    Permission, UserGroup
from .grouphierarchy import GroupHierarchy

__all__ = ('User', )

class User(DeclarativeBase, object):
    """
    Cette classe contient les informations relatives à un utilisateur.

    @ivar user_name: Nom de l'utilisateur (identifiant).
    @ivar fullname: Nom complet de l'utilisateur.
    @ivar email: Adresse email de l'utilisateur.
    @ivar password: Mot de passe (chiffré) de l'utilisateur.
    @ivar language: Langage utilisé par l'utilisateur.
    @ivar last_changed: Date de dernière mise à jour des informations
        de l'utilisateur.
    @ivar customgraphviews: Liste des vues personnalisées de l'utilisateur
        dans VigiGraph.
    @ivar usergroups: Liste des groupes d'utilisateurs auxquels
        l'utilisateur courant appartient.
    """

    __tablename__ = 'user'

    # XXX Faut-il renommer ce champ ?
    user_name = Column(
        Unicode(255),
        unique=True,
        primary_key=True,
    )

    fullname = Column(
        Unicode(255),
        nullable=False,
    )

    email = Column(
        Unicode(255),
        unique=True, index=True, nullable=False,
    )

    _password = Column(
        'password', Unicode(64),
        nullable=True,
    )

    # Language code using the format from RFC 4646.
    # See also http://www.ietf.org/rfc/rfc4646.txt
    _language = Column(
        # The 42 characters limit matches the minimal requirement
        # from RFC 4646 (4.3.1).
        'language', Unicode(42),
        nullable=True,
        default=None,
    )

    # XXX Rendre cet attribute obligatoire (nullable=False).
    last_changed = Column(
        DateTime(timezone=False),
#        nullable=False,
    )

    customgraphviews = relation('CustomGraphView',
        cascade='delete', lazy=True)

    usergroups = relation('UserGroup', secondary=USER_GROUP_TABLE,
        back_populates='users', lazy=True)


    def __init__(self, **kwargs):
        """
        Initialise l'instance avec les informations de l'utilisateur.
        
        @param kwargs: Un dictionnaire contenant les informations sur
            l'utilisateur.
        @type kwargs: C{dict}
        """
        super(User, self).__init__(**kwargs)

    def __unicode__(self):
        """
        Conversion en unicode.
        
        @return: Le nom de l'utilisateur.
        @rtype: C{str}
        """
        return self.user_name

    @property
    def permissions(self):
        """
        Renvoie un ensemble de chaînes de caractères indiquant les permissions
        associées à l'utilisateur.

        @return: Les permissions de cet utilisateur.
        @rtype: C{set} of C{str}       
        """
        perms = set()
        for g in self.usergroups:
            perms = perms | set(g.permissions)
        return perms


    def supitemgroups(self, drill_up=False):
        """
        Renvoie la liste des identifiants des groupes d'éléments supervisés
        auxquels l'utilisateur a accès.

        Les groupes sont récursifs.
        On suppose que l'attribut drill_up est mis à True.
        Si le groupe HG1 hérite du groupe HG et que l'utilisateur
        a les permissions sur le groupe HG1, alors il reçoit aussi
        (automatiquement) l'accès aux éléments rattachés à HG.

        Autrement dit:
        HG <- lié à un hôte H
        ^
        |
        HG1 <- lié à un hôte H1

        Si l'utilisateur U a les permissions sur HG (mais pas sur HG1),
        et l'utilisateur U1 a les permissions sur HG1 (mais pas sur HG).
        Alors U ne peut voir que les hôtes rattachés à HG (ici, H),
        tandis que U1 peut voir les hôtes rattachés soit à HG, soit à HG1
        (ou aux deux), c'est-à-dire H et H1.

        @param drill_up: Indique le sens de parcours du graphe.
            Si cette valeur vaut True, le parcours se fait du bas du graphe
            (des feuilles) vers le haut. Sinon (par défaut), il se fait du
            haut de l'arbre vers le bas (vers les feuilles).
        @type drill_up: C{bool}
        @return: Liste des identifiants des groupes d'éléments supervisés
            auxquels l'utilisateur a accès.
        @rtype: C{list} of C{int}
        """
        joins = []

        # En théorie, on devrait faire une jointure intermédiaire
        # sur un 2ème SupItemGroup. Ici, on peut l'éviter, ce qui
        # simplifie la requête SQL générée d'une part et simplifie
        # le code Python d'autre part (évite l'ajout d'aliases).
        if drill_up:
            joins.extend([
                (GroupHierarchy, GroupHierarchy.idparent == \
                    SupItemGroup.idgroup),
                (GROUP_PERMISSION_TABLE, GROUP_PERMISSION_TABLE.c.idgroup == \
                    GroupHierarchy.idchild),
            ])
        else:
            joins.extend([
                (GroupHierarchy, GroupHierarchy.idchild == \
                    SupItemGroup.idgroup),
                (GROUP_PERMISSION_TABLE, GROUP_PERMISSION_TABLE.c.idgroup == \
                    GroupHierarchy.idparent),
            ])

        joins.extend([
                (Permission, Permission.idpermission == \
                    GROUP_PERMISSION_TABLE.c.idpermission),
                (USERGROUP_PERMISSION_TABLE, \
                    USERGROUP_PERMISSION_TABLE.c.idpermission == \
                    Permission.idpermission),
                (UserGroup, UserGroup.idgroup == \
                    USERGROUP_PERMISSION_TABLE.c.idgroup),
                (USER_GROUP_TABLE, USER_GROUP_TABLE.c.idgroup == \
                    UserGroup.idgroup),
        ])

        groups = DBSession.query(
                SupItemGroup.idgroup
            ).join(*joins).filter(
                USER_GROUP_TABLE.c.username == self.user_name
            ).all()
        return [g.idgroup for g in groups]

    @property
    def groups(self):
        """
        Renvoie l'ensemble des identifiants des groupes
        d'hôtes / services / cartes auxquels l'utilisateur a accès.

        Les groupes sont récursifs.
        Si le groupe HG1 hérite du groupe HG et que l'utilisateur
        a les permissions sur le groupe HG1, alors il reçoit aussi
        (automatiquement) l'accès aux éléments rattachés à HG.

        Autrement dit:
        HG <- lié à un hôte H
        |
        HG1 <- lié à un hôte H1

        Si l'utilisateur U a les permissions sur HG (mais pas sur HG1),
        et l'utilisateur U1 a les permissions sur HG1 (mais pas sur HG).
        Alors U ne peut voir que les hôtes rattachés à HG (ici, H),
        tandis que U1 peut voir les hôtes rattachés soit à HG, soit à HG1
        (ou aux deux), c'est-à-dire H et H1.

        @return: Les groupes auxquels l'utilisateur a accès.
        @rtype: C{set} of C{Group}
        """
        groups = set()
        for ug in self.usergroups:
            for p in ug.permissions:
                # MapGroup
                for g in p.mapgroups:
                    node = g
                    while not node is None:
                        groups = groups | set([node.idgroup])
                        node = node.parent
        return groups

    def mapgroups(self, only_id=True):
        """
        Renvoie l'ensemble des groupes ou identifiants de groupe
        de cartes auxquels l'utilisateur a accès.

        Les groupes sont récursifs.
        Si le groupe HG1 hérite du groupe HG et que l'utilisateur
        a les permissions sur le groupe HG1, alors il reçoit aussi
        (automatiquement) l'accès aux éléments rattachés à HG.

        Autrement dit:
        HG <- lié à un hôte H
        |
        HG1 <- lié à un hôte H1

        Si l'utilisateur U a les permissions sur HG (mais pas sur HG1),
        et l'utilisateur U1 a les permissions sur HG1 (mais pas sur HG).
        Alors U ne peut voir que les hôtes rattachés à HG (ici, H),
        tandis que U1 peut voir les hôtes rattachés soit à HG, soit à HG1
        (ou aux deux), c'est-à-dire H et H1.
        
        @param only_id: Indique le type de retour de la fonction.
        Si cette valeur vaut True, la fonction renvoit la liste 
        des identifiants de groupe.
        Sinon, la fonction renvoie la liste des groupes 
        @type only_id: C{bool}

        @return: Les groupes de cartes auxquels l'utilisateur a accès.
        @rtype: C{set} of C{Group}
        """
        
        joins = []

        # En théorie, on devrait faire une jointure intermédiaire
        # sur un 2ème MapGroup. Ici, on peut l'éviter, ce qui
        # simplifie la requête SQL générée d'une part et simplifie
        # le code Python d'autre part (évite l'ajout d'aliases).
        
        joins.extend([
                (GroupHierarchy, GroupHierarchy.idparent == \
                    MapGroup.idgroup),
                (GROUP_PERMISSION_TABLE, GROUP_PERMISSION_TABLE.c.idgroup == \
                    GroupHierarchy.idchild),
            ])
        """
        joins.extend([
            (GroupHierarchy, GroupHierarchy.idchild == \
                MapGroup.idgroup),
            (GROUP_PERMISSION_TABLE, GROUP_PERMISSION_TABLE.c.idgroup == \
                GroupHierarchy.idparent),
        ])
        """

        joins.extend([
                (Permission, Permission.idpermission == \
                    GROUP_PERMISSION_TABLE.c.idpermission),
                (USERGROUP_PERMISSION_TABLE, \
                    USERGROUP_PERMISSION_TABLE.c.idpermission == \
                    Permission.idpermission),
                (UserGroup, UserGroup.idgroup == \
                    USERGROUP_PERMISSION_TABLE.c.idgroup),
                (USER_GROUP_TABLE, USER_GROUP_TABLE.c.idgroup == \
                    UserGroup.idgroup),
        ])

        groups = DBSession.query(
                MapGroup
            ).join(*joins).filter(
                USER_GROUP_TABLE.c.username == self.user_name
            ).order_by(MapGroup.name).all()
            
        if only_id:
            return [g.idgroup for g in groups]
        else:
            return groups
        
    def mapgroups_one_parent_max(self, only_id=True):
        """
        TODO: fonction à supprimer si inutilisée (utiliser plutôt mapgroups)
        Renvoie l'ensemble des groupes ou identifiants de groupe
        de cartes auxquels l'utilisateur a accès.

        Les groupes sont récursifs.
        Si le groupe HG1 hérite du groupe HG et que l'utilisateur
        a les permissions sur le groupe HG1, alors il reçoit aussi
        (automatiquement) l'accès aux éléments rattachés à HG.

        Autrement dit:
        HG <- lié à un hôte H
        |
        HG1 <- lié à un hôte H1

        Si l'utilisateur U a les permissions sur HG (mais pas sur HG1),
        et l'utilisateur U1 a les permissions sur HG1 (mais pas sur HG).
        Alors U ne peut voir que les hôtes rattachés à HG (ici, H),
        tandis que U1 peut voir les hôtes rattachés soit à HG, soit à HG1
        (ou aux deux), c'est-à-dire H et H1.
        
        @param only_id: Indique le type de retour de la fonction.
        Si cette valeur vaut True, la fonction renvoit la liste 
        des identifiants de groupe.
        Sinon, la fonction renvoie la liste des groupes 
        @type only_id: C{bool}

        @return: Les groupes de cartes auxquels l'utilisateur a accès.
        @rtype: C{set} of C{Group}
        """
        
        groups = set()
        for ug in self.usergroups:
            for p in ug.permissions:
                # MapGroup
                for g in p.mapgroups:
                    node = g
                    while not node is None:
                        groups = groups | set([node])
                        node = node.get_parent()
            
        if only_id:
            return [g.idgroup for g in groups]
        else:
            return groups
           
    
    def maps(self, only_id=True):
        """
        Renvoie l'ensemble des identifiants des cartes
        auxquelles l'utilisateur a accès.

        @return: Les cartes auxquelles l'utilisateur a accès.
        @rtype: C{set} of C{int}
        """
        maps = set()
        for ms in [group.maps for group in self.mapgroups(False)]:
            for m in ms:
                maps = maps | set([m])
        for ug in self.usergroups:
            for p in ug.permissions:
                # Map
                for m in p.maps:
                    maps = maps | set([m])
                    
        if only_id:
            return [m.idmap for m in maps]
        else:
            return maps

    @classmethod
    def by_email_address(cls, email):
        """
        Retourne l'utilisateur (L{User}) dont l'adresse email
        est L{email}.
        
        @return: Utilisateur dont l'email est L{email}.
        @rtype: L{User}
        """
        return DBSession.query(cls).filter(cls.email == email).first()

    @classmethod
    def by_user_name(cls, username):
        """
        Retourne l'utilisateur (L{User}) dont le nom d'utilisateur
        est L{username}.
        
        @return: Utilisateur dont le nom d'utilisateur est L{username}.
        @rtype: L{User}
        """
        return DBSession.query(cls).filter(cls.user_name == username).first()


    def _set_password(self, password):
        """
        Attribue le mot de passe donné à l'utilisateur.

        Le mot de passe n'est pas stocké dans la base de données mais est géré
        par une source quelconque. L'utilisateur peut simplement le modifier ou
        comparer un texte avec le mot de passe.

        @param password: Le nouveau mot de passe de l'utilisateur.
        @type password: C{str}
        """
        self._password = self._hash_password(password)

    def validate_password(self, password):
        """
        Teste si le mot de passe proposé correspond au mot de passe de
        l'utilisateur.
        
        @param password: Le mot de passe donné par l'utilisateur pour
            s'authentifier, en texte clair.
        @type password: C{str}
        @return: Un booléen indiquant si le mot de passe est correct.
        @rtype: C{bool}
        """

        try:
            from tg import config
            from paste.deploy.converters import asbool
        except ImportError:
            # TurboGears n'est pas utilisé,
            # on utilise vigilo.common.conf
            # et on convertit en booléen
            # depuis l'objet ConfigObj.
            from vigilo.common.conf import settings
            settings.load_module(__name__)
            config = settings['database']
            if config.has_key('use_kerberos') and \
                config.as_bool('use_kerberos'):
                return True
        else:
            # Dans le cas où on utilise la configuration
            # de TurboGears, on doit utiliser paste.deploy
            # pour convertir en booléen.
            if asbool(config.get('use_kerberos', True)):
                return True

        # Petite précaution
        if self._password is None:
            return False
        return self._hash_password(password) == self._password

    @staticmethod
    def _hash_password(password):
        """
        Applique une fonction de hachage au mot de passe.
        
        @param password: Mot de passe à hacher.
        @type password: C{str}
        @return: Hash correspondant au mot de passe donné.
        @rtype: 
        @note: Si la variable HASH_FUNCTION a été définie dans la configuration,
            la méthode correspondante du module C{hashlib} est utilisée.
            Si la variable n'existe pas ou ne correspond pas à une classe
            valide du module hashlib, alors le mot de passe est stocké en clair.
        """

        try:
            from tg import config
        except ImportError:
            from vigilo.common.conf import settings
            settings.load_module(__name__)
            config = settings['database']

        hash_method = config.get('password_hashing_function')
        if not hash_method is None:
            hash_method = hashlib.__dict__.get(hash_method)
            if not callable(hash_method):
                hash_method = None

        if hash_method is None:
            return password
        return u'' + hash_method(password).hexdigest()

    password = synonym('_password', descriptor=property(None,
                                                        _set_password))

    def _set_language(self, language):
        """
        Change la langue de l'utilisateur.

        @param language: La nouvelle langue de l'utilisateur.
        @type language: C{str}
        """
        self._language = language

    def _get_language(self):
        """
        Renvoie la langue préférée de l'utilisateur.

        Si l'utilisateur n'a pas choisi sa langue, la langue par défaut
        dans la configuration est renvoyée.

        :return: La langue préférée de l'utilisateur.
        :rtype: C{str}
        """

        try:
            from tg import config
        except ImportError:
            from vigilo.common.conf import settings
            settings.load_module(__name__)
            config = settings['database']

        if self._language is None:
            language = config.get('lang')
            if language is None:
                raise KeyError, "No default language in settings"
            return language
        return self._language

    language = synonym('_language', descriptor=property(_get_language,
                                                        _set_language))

