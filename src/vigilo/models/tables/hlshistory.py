# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2013 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèle pour la table HLSHistory."""
from sqlalchemy import Column
from sqlalchemy.types import Integer, DateTime
from sqlalchemy.orm import relation

from vigilo.models.session import DeclarativeBase, ForeignKey
from vigilo.models.tables import HighLevelService, StateName

__all__ = ('HLSHistory', )

class HLSHistory(DeclarativeBase, object):
    """
    Cette classe stocke les informations sur les changements d'états
    des services de haut niveau.
    Elle joue un rôle similaire à EventHistory, mais n'a pas de
    dépendances sur les événements (L{Event}) car ceux-ci ne concernent
    de toutes façons que les L{Host} et les L{LowLevelService}.
    """
    __tablename__ = 'hlshistory'

    idhistory = Column(
        Integer,
        primary_key=True, 
        autoincrement=True,
    )

    idhls = Column(
        Integer,
        ForeignKey(
            HighLevelService.idservice,
            onupdate='CASCADE',
            ondelete='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        autoincrement=False,
        nullable=False,
    )

    hls = relation('HighLevelService', lazy=True)

    timestamp = Column(
        DateTime(timezone=False),
        nullable=False,
    )

    idstatename = Column(
        Integer,
        ForeignKey(
            StateName.idstatename,
            deferrable=True,
            initially='IMMEDIATE',
        )
    )

    statename = relation('StateName', lazy=True)

    def __init__(self, **kwargs):
        """
        Initialise une entrée d'historique concernant le changement
        d'état d'un service de haut niveau.
        """
        super(HLSHistory, self).__init__(**kwargs)

