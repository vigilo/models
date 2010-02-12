# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table PerfDataSource"""
from sqlalchemy import Column
from sqlalchemy.orm import relation
from sqlalchemy.types import Integer, UnicodeText, Float

from vigilo.models.configure import DeclarativeBase, ForeignKey
from vigilo.models.secondary_tables import GRAPH_PERFDATASOURCE_TABLE
from vigilo.models.service import LowLevelService

__all__ = ('PerfDataSource', )

class PerfDataSource(DeclarativeBase, object):
    """
    Informations sur une source de donnée d'un service.

    @ivar idperfdatasource: Identifiant auto-généré de la source de données.
    @ivar name: Nom de la source de données.
    @ivar type: Type de la source de données
        (COUNTER, DERIVE, ABSOLUTE, GAUGE).
    @ivar label: Label affiché sur le graphique.
        (ex name=ineth0 -> label=Données en entrée sur la carte réseau eth0)
    @ivar factor: Facteur de multiplication pour les valeurs stockés.
        (ex factor=8 pour conversion octets -> bits)
    """

    __tablename__ = 'perfdatasource'

    idperfdatasource = Column(
        Integer,
        primary_key=True, autoincrement=True,
    )

    idservice = Column(
        Integer,
        ForeignKey(
            LowLevelService.idservice,
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        nullable=False,
    )

    service = relation('LowLevelService')
    
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
        """Initialisation de la source de données de performance."""
        super(PerfDataSource, self).__init__(**kwargs)

