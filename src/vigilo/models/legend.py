# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Host"""
from __future__ import absolute_import

from sqlalchemy import Column
from sqlalchemy.types import Integer, Unicode, UnicodeText
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relation

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .session import DBSession

__all__ = ('Legend', )

class Legend(DeclarativeBase, object):
    """
    Informations sur Legende
    
    @ivar minthreshold: Seuil minimum.
    @ivar fillcolor: Couleur de remplissage.
    @ivar strokecolor: Couleur de bordure.
    """
    __tablename__ = bdd_basename + 'legend'

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
