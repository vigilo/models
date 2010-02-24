# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table User"""
from sqlalchemy.orm import synonym, relation
from sqlalchemy import Column
from sqlalchemy.types import Unicode, DateTime
import hashlib

from vigilo.models.configure import DeclarativeBase, DBSession
from vigilo.models.secondary_tables import USER_GROUP_TABLE

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

    @property
    def groups(self):
        """
        Renvoie l'ensemble des identifiants des groupes
        d'hôtes / services / cartes auxquels l'utilisateur a accès.

        @return: Les groupes auxquels l'utilisateur a accès.
        @rtype: C{set} of C{Group}
        """
        groups = set()
        for ug in self.usergroups:
            for p in ug.permissions:
                # HostGroup
                for g in p.hostgroups:
                    node = g
                    while not node is None:
                        groups = groups | set([node.idgroup])
                        node = node.parent

                # MapGroup
                for g in p.mapgroups:
                    node = g
                    while not node is None:
                        groups = groups | set([node.idgroup])
                        node = node.parent

                # ServiceGroup
                for g in p.servicegroups:
                    node = g
                    while not node is None:
                        groups = groups | set([node.idgroup])
                        node = node.parent
        return groups

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
        except ImportError:
            from vigilo.common.conf import settings
            settings.load_module(__name__)
            config = settings['database']

        try:
            if config.has_key('use_kerberos') and \
                config.as_bool('use_kerberos'):
                return True
        except AttributeError:
            pass

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

