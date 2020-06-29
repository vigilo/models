# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2020 CS GROUP – France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèle pour la table User"""
import hashlib, random

from sqlalchemy import Column
from sqlalchemy.orm import synonym, relation
from sqlalchemy.types import Unicode, DateTime, String
from passlib.context import CryptContext

from vigilo.models.session import DeclarativeBase, DBSession
from vigilo.models.tables.secondary_tables import USER_GROUP_TABLE
from vigilo.models.tables import SupItemGroup, UserGroup, MapGroup, \
                                    DataPermission
from vigilo.models.tables.grouphierarchy import GroupHierarchy

__all__ = ('User', )

class User(DeclarativeBase, object):
    """
    Cette classe contient les informations relatives à un utilisateur.

    @ivar user_name: Nom de l'utilisateur (identifiant).
    @ivar fullname: Nom complet de l'utilisateur.
    @ivar email: Adresse email de l'utilisateur.
    @ivar password: Mot de passe de l'utilisateur.
        Le format exact (haché ou clair, présence ou non de sel,
        nombre d'itérations de l'algorithme, etc.) dépend des options
        de configuration.
    @ivar language: Langage utilisé par l'utilisateur.
    @ivar last_changed: Date de dernière mise à jour des informations
        de l'utilisateur.
    @ivar usergroups: Liste des groupes d'utilisateurs auxquels
        l'utilisateur courant appartient.
    """

    __tablename__ = 'vigilo_user'

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
        index=True,
        nullable=True,
    )

    _password = Column(
        'password', String(256),
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

    usergroups = relation('UserGroup', secondary=USER_GROUP_TABLE,
        back_populates='users', lazy=True, order_by='UserGroup.group_name')

    def _generate_token(self):
        # MD5 est utilisé ici uniquement parce qu'il est également disponible
        # côté SGBD et utilisé ainsi par le script de migration.
        return unicode(hashlib.md5(str(random.random())).hexdigest())

    # Le token est généré automatiquement à la volée.
    token = Column(
        Unicode(32),
        nullable=True,
        default=_generate_token,
    )

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


    def supitemgroups(self, access=None):
        """
        Renvoie la liste des identifiants des groupes d'éléments supervisés
        auxquels l'utilisateur a accès.

        @param access: La liste des types d'accès qui autoriseront
            l'utilisateur à voir les groupes. Si elle vaut C{None},
            aucune vérification n'est faite sur le type d'accès.
        @param access: C{basestring} or C{list} of C{basestring}

        @return: Liste des identifiants des groupes d'éléments supervisés
            auxquels l'utilisateur a accès.
        @rtype: C{list} of Ctuple{} of C{int}, C{bool}
        """
        result = {}
        if hasattr(access, '__iter__'):
            access = set([ unicode(a) for a in access ])
        elif access is not None:
            access = set([unicode(access)])

        # L'accès en écriture donne implicitement un accès en lecture.
        if access is not None and u'r' in access:
            access.add(u'w')

        # Groupes d'éléments supervisés auxquels
        # l'utilisateur a directement accès.
        direct = DBSession.query(SupItemGroup.idgroup).distinct(
            ).join(
                (GroupHierarchy, GroupHierarchy.idchild ==
                    SupItemGroup.idgroup),
                (DataPermission, DataPermission.idgroup ==
                    GroupHierarchy.idparent),
                (UserGroup, UserGroup.idgroup == DataPermission.idusergroup),
                (USER_GROUP_TABLE, USER_GROUP_TABLE.c.idgroup ==
                    UserGroup.idgroup),
            ).filter(USER_GROUP_TABLE.c.username == self.user_name)
        if access is not None:
            direct = direct.filter(DataPermission.access.in_(access))
        direct = direct.all()
        direct_ids = [sig.idgroup for sig in direct]

        # Groupes d'éléments supervisés auxquels l'utilisateur a accès
        # indirectement (droit de passage, mais pas de droit de lecture).
        indirect = DBSession.query(SupItemGroup.idgroup).distinct(
            ).join(
                (GroupHierarchy, GroupHierarchy.idparent == \
                    SupItemGroup.idgroup),
            ).filter(GroupHierarchy.idchild.in_(direct_ids)
            ).filter(GroupHierarchy.hops > 0
            ).all()

        for sig in indirect:
            result[sig.idgroup] = (sig.idgroup, False)
        for sig in direct:
            result[sig.idgroup] = (sig.idgroup, True)

        return result.values()

    def mapgroups(self, only_id=True, only_direct=False, access=None):
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
            Si cette valeur vaut True, la fonction renvoie la liste
            des identifiants de groupe.
            Sinon, la fonction renvoie la liste des groupes
        @type only_id: C{bool}

        @param only_direct: Indique si on retourne uniquement
            les groupes de cartes auxquels l'utilisateur a directement
            accés ou tous les groupes, y compris ceux auxquels il a
            indirectement accés (droit de passage, mais pas de droit
            de lecture)
        @type only_direct: C{bool}

        @param access: La liste des types d'accès qui autoriseront
            l'utilisateur à voir les groupes. Si elle vaut C{None},
            aucune vérification n'est faite sur le type d'accès.
        @param access: C{basestring} or C{list} of C{basestring}

        @return: Les groupes de cartes auxquels l'utilisateur a accès.
        @rtype: C{list} of C{int} if L{only_id} is True, C{list} of C{Group}
            otherwise.
        """
        columns = None

        if hasattr(access, '__iter__'):
            access = set([ unicode(a) for a in access ])
        elif access is not None:
            access = set([unicode(access)])

        # L'accès en écriture donne implicitement un accès en lecture.
        if access is not None and u'r' in access:
            access.add(u'w')

        if only_id:
            columns = MapGroup.idgroup
        else:
            columns = MapGroup

        # Groupes de cartes auxquels l'utilisateur a directement accès.

        direct = DBSession.query(columns).distinct(
            ).join(
                (GroupHierarchy, GroupHierarchy.idchild == MapGroup.idgroup),
                (DataPermission, DataPermission.idgroup ==
                    GroupHierarchy.idparent),
                (UserGroup, UserGroup.idgroup == DataPermission.idusergroup),
                (USER_GROUP_TABLE, USER_GROUP_TABLE.c.idgroup ==
                    UserGroup.idgroup),
            ).filter(USER_GROUP_TABLE.c.username == self.user_name)
        if access is not None:
            direct = direct.filter(DataPermission.access.in_(access))
        direct = direct.all()
        direct_ids = [mg.idgroup for mg in direct]

        # Groupes de cartes auxquels l'utilisateur a accès indirectement
        # (droit de passage, mais pas de droit de lecture).
        indirect = DBSession.query(columns).distinct(
            ).join(
                (GroupHierarchy, GroupHierarchy.idparent == MapGroup.idgroup),
            ).filter(GroupHierarchy.idchild.in_(direct_ids)
            ).all()

        groups = None
        if only_direct:
            groups = direct
        else:
            groups = indirect

        if only_id:
            return [g.idgroup for g in groups]
        else:
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
        Modifie le mot de passe de l'utilisateur.

        @param password: Nouveau mot de passe de l'utilisateur (en clair).
            Le mot de passe sera haché avant d'être stocké en base de données.
        @type password: C{str}
        """
        from vigilo.models.configure import SCHEMES as schemes
        ctx = CryptContext(schemes=schemes)

        # Supporte l'API de Passlib 1.7.0+ (méthode hash())
        # et celle des versions antérieures (méthode encrypt()).
        if hasattr(ctx, 'hash'):
            self._password = ctx.hash(password)
        else:
            self._password = ctx.encrypt(password)

    def validate_password(self, password, allow_missing=False):
        """
        Teste si le mot de passe proposé correspond au mot de passe de
        l'utilisateur.

        @param password: Le mot de passe donné par l'utilisateur pour
            s'authentifier, en texte clair.
        @type password: C{str}
        @param allow_missing: Indique si un mot de passe absent
            dans la base de données donne systématiquement accès
            ou si au contraire il refuse systématiquement l'accès.
        @type allow_missing: C{bool}
        @return: Un booléen indiquant si le mot de passe est correct.
        @rtype: C{bool}
        """
        # Petite précaution : si aucun mot de passe n'a été défini,
        # on laisse l'appelant décider du comportement à adopter.
        # Par défaut, la validation échouera systématiquement.
        if self._password is None:
            return bool(allow_missing)

        from vigilo.models.configure import SCHEMES as schemes
        from vigilo.models.configure import DEPRECATED_SCHEMES as \
            deprecated_schemes

        ctx = CryptContext(schemes=schemes, deprecated=deprecated_schemes)
        valid, new_hash = ctx.verify_and_update(password, self._password)
        if not valid:
            return False
        if new_hash:
            self._password = new_hash
        return True

    # Définition des accesseurs pour le (haché du) mot de passe.
    # Empêche la lecture directe et applique la méthode de hachage
    # en cas de changement du mot de passe par l'utilisateur.
    password = synonym('_password', descriptor=property(lambda obj: u'', _set_password))

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
        from vigilo.models.configure import DEFAULT_LANG
        if self._language is not None:
            return self._language

        if not DEFAULT_LANG:
            raise KeyError("No default language in settings")
        return DEFAULT_LANG

    language = synonym('_language', descriptor=property(_get_language,
                                                        _set_language))

    def renew_token(self):
        self.token = self._generate_token()
