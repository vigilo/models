# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2015 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèle pour la table Application."""
from sqlalchemy import Column
from sqlalchemy.types import Unicode, Integer

from vigilo.models.session import DeclarativeBase, DBSession

__all__ = ('Application', )

class Application(DeclarativeBase, object):
    """
    Gère les applications employées par Vigilo.

    @ivar idapp: Identifiant de l'application.
    @ivar name: Nom (unique) de l'application.
    """
    __tablename__ = 'application'

    idapp = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name = Column(
        Unicode(255),
        nullable=False,
        unique=True,
    )

    def __init__(self, **kwargs):
        """
        Initialise l'instance avec les informations de l'application.

        @param kwargs: Un dictionnaire contenant les informations sur
            l'applications.
        @type kwargs: C{dict}
        """
        super(Application, self).__init__(**kwargs)

    def __unicode__(self):
        """
        Conversion en unicode.

        @return: Nom du groupe d'applications.
        @rtype: C{unicode}
        """
        return self.name

    def __str__(self):
        return str(self.name)


    @classmethod
    def by_app_name(cls, app):
        """Renvoie une instance d'L{Application} à partir de son nom."""
        return DBSession.query(cls).filter(cls.name == app).first()

