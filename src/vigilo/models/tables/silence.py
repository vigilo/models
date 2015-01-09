# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2015 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèle pour la table Silence"""
from sqlalchemy import Column
from sqlalchemy.orm import relation
from sqlalchemy.types import Text, DateTime, Integer, Unicode

from vigilo.models.session import DeclarativeBase, ForeignKey
from vigilo.models.tables.supitem import SupItem
from vigilo.models.tables.user import User
from vigilo.models.tables.secondary_tables import SILENCE_STATE_TABLE

__all__ = ('Silence', )

class Silence(DeclarativeBase, object):
    """
    Règle de mise en silence.

    @ivar idsilence: Identifiant de la mise en silence.
    @ivar idsupitem: Identifiant de l'item (hôte ou service)
        mis en silence.
    @ivar supitem: Instance de l'élément supervisé mis en silence.
    @ivar lastmodification: Date de dernière modification de la règle.
    @ivar author: Utilisateur ayant créé cette règle.
    @ivar comment: Commentaire ajouté par l'utilisateur.
#    @ivar start: Date de début de la mise en silence.
#    @ivar end: Date de fin de la mise en silence.
    @ivar states: Liste des états (L{StateName}) concernés par la règle.
    """

    __tablename__ = 'silence'

    idsilence = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )

    idsupitem = Column(
        Integer,
        ForeignKey(
            SupItem.idsupitem,
            onupdate='CASCADE',
            ondelete='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        nullable=False,
    )

    supitem = relation('SupItem')

    lastmodification = Column(DateTime(timezone=False), nullable=False)

    author = Column(
        Unicode(255),
        ForeignKey(
            User.user_name,
            onupdate='CASCADE',
            ondelete='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        nullable=False,
    )

    user = relation('User')

    comment = Column(Text, nullable=True)

#    start = Column(DateTime(timezone=False), nullable=False)
#
#    end = Column(DateTime(timezone=False), nullable=False)

    states = relation('StateName', secondary=SILENCE_STATE_TABLE, lazy=True)
#        back_populates='idstatename', lazy=True)


    def __init__(self, **kwargs):
        """
        Initialisation.
        """
        super(Silence, self).__init__(**kwargs)

