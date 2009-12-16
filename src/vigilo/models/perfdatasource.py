# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table PerfDataSource"""
from __future__ import absolute_import

from sqlalchemy import ForeignKey, Column
from sqlalchemy.orm import relation
from sqlalchemy.types import Integer, UnicodeText, Float

from .vigilo_bdd_config import bdd_basename, DeclarativeBase

__all__ = ('PerfDataSource', )

class PerfDataSource(DeclarativeBase, object):
    """
    Informations sur une datasource d'un service.

    @ivar idperfdatasource: Identifiant de la datasource, autogénéré.
    @ivar name: Nom de la datasource.
    @ivar type: Type de la datasource (COUNTER, DERIVE, ABSOLUTE, GAUGE).
    @ivar label: Label affiché sur le graphique.
        (ex name=ineth0 -> label=Données en entrée sur la carte réseau eth0)
    @ivar factor: Facteur de multiplication pour les valeurs stockés.
        (ex factor=8 pour conversion octets -> bits)
    """

    __tablename__ = bdd_basename + 'perfdatasource'

    idperfdatasource = Column(
        Integer,
        primary_key=True, autoincrement=True,
    )

    idservice = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'servicelowlevel.idservice',
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        nullable=False,
    )

    service = relation('ServiceLowLevel')
    
    graphs = relation('Graph', secondary=GRAPH_PERFDATASOURCE_TABLE,
                         back_populates='perfdatasources', lazy=True)

    name = Column(
        UnicodeText,
        nullable=False)
    
    # GAUGE, COUNTER, ...
    type = Column(
        UnicodeText,
        default=u'', nullable=False)
    # pour l'affichage du nom sur le graphique généré
    label = Column(
        UnicodeText,
        default=u'')

    factor = Column(
        Float(precision=None, asdecimal=False),
        default=0.0, nullable=False)

    def __init__(self, **kwargs):
        super(PerfDataSource, self).__init__(**kwargs)

