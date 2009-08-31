# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table User"""
from __future__ import absolute_import

from sqlalchemy.orm import synonym
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
        UnicodeText(),
        primary_key=True)

    email = Column(
        UnicodeText(),
        unique=True)

    # Language code using the format from RFC 1766.
    _language = Column(
        'language',
        UnicodeText(),
        nullable=True,
        default=None)

    # We don't actually store the password in the database,
    # but we need to define it for Rum to be able to "see" it.
    _password = Column('password', Unicode(0),
                        nullable=True, default=None,
                        info={'rum': {'field': 'Password'}})


    def __init__(self, **kwargs):
        DeclarativeBase.__init__(self, **kwargs)

    def __unicode__(self):
        return self.user_name

    @property
    def permissions(self):
        """Return a set of strings for the permissions granted."""
        perms = set()
        for g in self.groups:
            perms = perms | set(g.permissions)
        return perms

    @classmethod
    def by_email_address(cls, email):
        """Return the user object whose email address is ``email``."""
        return DBSession.query(cls).filter(cls.email==email).first()

    @classmethod
    def by_user_name(cls, username):
        """Return the user object whose user name is ``username``."""
        return DBSession.query(cls).filter(cls.user_name==username).first()



    # @TODO adapt this method to set the password remotely.
    def _set_password(self, password):
        """
        Sets the user's password to the new password given.

        Where the password actually gets stored is configuration dependent.
        This method delegates the actual operation to the proper method.

        :param password: the new password for the current user.
        :type password: unicode object
        """
        pass

    def _get_password(self):
        """
        Returns a dummy value for password.

        The password must be considered write-only event though you can
        validate a user using validate_password (see below).

        Returns a dummy value makes Rum hide the column in display screens,
        while still allowing for edition.
        """
        return '[Hidden]'

    # @TODO adapt this method to authenticate against a remote source.
    def validate_password(self, password):
        """
        Check the password against existing credentials.
        
        :param password: the password that was provided by the user to
            try and authenticate. This is the clear text version that we will
            need to match against the one we have in store.
        :type password: unicode object
        :return: Whether the password is valid.
        :rtype: bool

        """
        return password == '42'

    password = synonym('_password', descriptor=property(_get_password,
                                                        _set_password))

    def _set_language(self, language):
        """
        Sets the user's language.

        :param language: the new language to use with the current user.
        :type language: unicode object
        """
        self._language = language

    def _get_language(self):
        """
        Returns the language to use to communicate with this user.

        If no language has been chosen by this user, a default one is taken
        from the configuration settings.

        :return: The language to use to communicate with this user.
        :rtype: unicode object
        """
        if self._language is None:
            language = settings['VIGILO_ALL_DEFAULT_LANGUAGE']
            if language is None:
                raise KeyError, "No default language in settings"
            return language
        return self._language

    language = synonym('_language', descriptor=property(_get_language,
                                                        _set_language))

