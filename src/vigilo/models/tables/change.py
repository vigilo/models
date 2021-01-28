# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2021 CS GROUP - France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèle pour la table Change"""
from sqlalchemy import Column
from sqlalchemy.types import Unicode, DateTime

from datetime import datetime

from vigilo.models.session import DeclarativeBase, DBSession

__all__ = ('Change', )

class Change(DeclarativeBase, object):
    """
    Mémorise la date de dernière modification d'un élément.
    Par élément, on entend un code qui permet de distinguer
    les différents composants dont les dates de dernières
    modifications nous intéressent.
    Ex : un nom de table SQL, un nom d'application, une fonction, etc.

    @ivar element: Nom de la table.
    @ivar last_modified: Date de dernière modification.
    """
    __tablename__ = 'vigilo_change'

    element = Column(
        Unicode(255),
        index=True, primary_key=True,
    )

    last_modified = Column(
        DateTime(timezone=False),
        nullable=False,
    )


    def __init__(self, **kwargs):
        """Initialise un modification de table."""
        super(Change, self).__init__(**kwargs)

    def __unicode__(self):
        """
        Représentation d'un C{Change}.

        @return: Le nom de la table concernée.
        @rtype: C{str}
        """
        return self.element

    @classmethod
    def by_table_name(cls, element):
        """
        Renvoie les informations concernant la dernière modification
        de l'élément L{element}.

        @param element: Nom de l'élément voulu.
        @type element: C{unicode}
        @return: Les informations concernant l'élément demandé.
        @rtype: L{Change}
        """
        return DBSession.query(cls).filter(cls.element == element).first()

    @classmethod
    def mark_as_modified(cls, element):
        """
        Marque un élément comme ayant été modifié.
        @param element: Nom de l'élement ayant subit une modification.
        @type element: C{unicode}
        """
        change = cls.by_table_name(element)

        if not change:
            change = cls(element=element)

        change.last_modified = datetime.utcnow()
        DBSession.add(change)
        DBSession.flush()
