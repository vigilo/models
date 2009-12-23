# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Change"""
from __future__ import absolute_import

from sqlalchemy import Column
from sqlalchemy.types import Unicode, DateTime

from datetime import datetime

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .session import DBSession

__all__ = ('Change', )

class Change(DeclarativeBase, object):
    """
    Mémorise la date de dernière modification d'une table.
    
    @ivar tablename: Nom de la table.
    @ivar last_modified: Date de dernière modification.
    """
    __tablename__ = bdd_basename + 'change'

    tablename = Column(
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
        return self.tablename

    @classmethod
    def by_table_name(cls, tablename):
        """
        Renvoie la modification se rapportant à la table L{tablename}.
        
        @param tablename: Nom de la table voulue.
        @type tablename: C{unicode}
        @return: Les informations de modification sur la table demandée.
        @rtype: L{Change}
        """
        return DBSession.query(cls).filter(cls.tablename == tablename).first()

    @classmethod
    def mark_as_modified(cls, tablename):
        """
        Marque une table comme ayant été modifiée.
        @param tablename: Nom de la table ayant subit une modification.
        @type tablename: C{unicode}
        """
        change = cls.by_table_name(tablename)

        if not change:
            change = cls(tablename=tablename)

        change.last_modified = datetime.now()
        DBSession.add(change)
        DBSession.flush()

