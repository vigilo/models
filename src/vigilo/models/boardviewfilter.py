# -*- coding: utf-8 -*-
"""Modèle pour la table BoardViewFilter."""
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relation
from sqlalchemy.types import Unicode, UnicodeText, Integer

from vigilo.models.configure import db_basename, DeclarativeBase

__all__ = ('BoardViewFilter', )

class BoardViewFilter(DeclarativeBase, object):
    """
    Gère les filtres personnalisés d'un utilisateur dans Vigiboard.
    Cette classe permet de remplir le formulaire de recherche
    de VigiBoard avec des valeurs prédéfinies. Elle reprend donc les
    différents champs de ce formulaire.

    @ivar filtername: Nom du filtre.
    @ivar username: Nom de l'utilisateur à qui appartient le filtre.
    @ivar message: Message issu de Nagios.
    @ivar trouble_ticket: Ticket d'incident.
    """

    __tablename__ = db_basename + 'boardviewfilter'

    filtername = Column(
        Unicode(255),
        primary_key=True, index=True, nullable=False)

    username = Column(
        Unicode(255),
        ForeignKey(
            db_basename + 'user.user_name',
            onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True, index=True, nullable=False)

    idservice = Column(
        Integer,
        ForeignKey(
            db_basename + 'lowlevelservice.idservice',
            onupdate='CASCADE', ondelete='CASCADE',
        ),
        nullable=False,
    )

    service = relation('LowLevelService')

    message = Column(UnicodeText)

    trouble_ticket = Column(UnicodeText)

    def __init__(self, **kwargs):
        """Initialise un filtre."""
        super(BoardViewFilter, self).__init__(**kwargs)

