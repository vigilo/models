# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2011-2015 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèle pour la table Host"""
from sqlalchemy import Column
from sqlalchemy.types import Integer, Unicode

from vigilo.models.session import DeclarativeBase

__all__ = ('Legend', )

class Legend(DeclarativeBase, object):
    """
    Informations sur Legende
    
    @ivar minthreshold: Seuil minimum.
    @ivar fillcolor: Couleur de remplissage.
    @ivar strokecolor: Couleur de bordure.
    """
    __tablename__ = 'legend'

    minthreshold = Column(
        Integer,
        primary_key=True,
        autoincrement=False
    )

    fillcolor = Column(
        Unicode(16),
        nullable=False)

    strokecolor = Column(
        Unicode(16),
        nullable=False)


    def __init__(self, **kwargs):
        """Initialise une Legende."""
        super(Legend, self).__init__(**kwargs)
