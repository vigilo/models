# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table User"""
from __future__ import absolute_import

from sqlalchemy.orm import synonym, relation
from sqlalchemy import Column
from sqlalchemy.types import Unicode, UnicodeText

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .session import DBSession
from vigilo.common.conf import settings

__all__ = ('User', )

class User(DeclarativeBase, object):
    """Stores information about users."""

    __tablename__ = bdd_basename + 'user'

    # TG2 expects this name.
    user_name = Column(
        Unicode(255),
        unique=True,
        primary_key=True,
        info={'rum': {'field': 'Text'}})

    email = Column(
        Unicode(255),
        unique=True,
        info={'rum': {'field': 'Email'}})

    # Language code using the format from RFC 4646.
    # See also http://www.ietf.org/rfc/rfc4646.txt
    _language = Column(
        # The 42 characters limit matches the minimal requirement
        # from RFC 4646 (4.3.1).
        'language', Unicode(42),
        nullable=True,
        default=None)

    # We don't actually store the password in the database,
    # but we need to define it for Rum to be able to "see" it.
    _password = Column(
        'password', Unicode(0),
        nullable=True, default=None,
        info={'rum': {'field': 'Password'}})


    customgraphviews = relation('CustomGraphView', cascade='delete',
        backref='user', lazy='dynamic')



    def __init__(self, **kwargs):
        """
        Initialise l'instance avec les informations de l'utilisateur.
        
        @param kwargs: Un dictionnaire contenant les informations sur
            l'utilisateur.
        @type kwargs: 
        """
        DeclarativeBase.__init__(self, **kwargs)

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
        Renvoie un ensemble de chaînes de caractères indiquant les groupes
        d'hôtes / services auxquels l'utilisateur a accès.

        @return: Les groupes auxquels l'utilisateur a accès.
        @rtype: C{set} of C{str}
        """
        groups = set()
        for ug in self.usergroups:
            for p in ug.permissions:
                for g in p.groups:
                    node = g
                    while not node is None:
                        groups = groups | set([node.name])
                        node = node.parent
        return groups

    @classmethod
    def by_email_address(cls, email):
        """
        Return the user object whose email address is C{email}.
        """
        return DBSession.query(cls).filter(cls.email == email).first()

    @classmethod
    def by_user_name(cls, username):
        """
        Return the user object whose user name is C{username}.
        """
        return DBSession.query(cls).filter(cls.user_name == username).first()



    # @TODO adapt this method to set the password remotely.
    def _set_password(self, password):
        """
        Attribue le mot de passe donné à l'utilisateur.

        Le mot de passe n'est pas stocké dans la base de données mais est géré
        par une source quelconque. L'utilisateur peut simplement le modifier ou
        comparer un texte avec le mot de passe.

        @param password: Le nouveau mot de passe de l'utilisateur.
        @type password: C{str}
        """
        pass

    def _get_password(self):
        """
        Retourne une constante en guise de mot de passe.

        Dans Vigilo, le mot de passe de l'utilisateur n'est pas stocké en base
        de données. À la place, il est stocké dans une source quelconque
        et n'est pas accessible en lecture.

        @return: La constante "[Hidden]".
        @rtype: C{str}
        """
        return '[Hidden]'

    # @TODO adapt this method to authenticate against a remote source.
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
        return password == '42'

    password = synonym('_password', descriptor=property(_get_password,
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
        if self._language is None:
            language = settings['VIGILO_ALL_DEFAULT_LANGUAGE']
            if language is None:
                raise KeyError, "No default language in settings"
            return language
        return self._language

    language = synonym('_language', descriptor=property(_get_language,
                                                        _set_language))

