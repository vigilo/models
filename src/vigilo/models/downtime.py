# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Downtime"""
from __future__ import absolute_import

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relation
from sqlalchemy.types import Text, DateTime, Integer, Unicode

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .session import DBSession

__all__ = ('Downtime', )

class Downtime(DeclarativeBase, object):
    """
    Mise en silence durant une maintenance.

    @ivar iddowntime: Identifiant de la mise en maintenance.
    @ivar idsupitem: Identifiant de l'item (hôte ou service) 
        mis en maintenance.
    @ivar supitem: Instance de l'élément supervisé placé en maintenance.
    @ivar entrytime: Date d'ajout de la mise en maintenance dans Vigilo.
    @ivar author: Utilisateur ayant créé cette mise en maintenance 
        dans Vigilo.
    @ivar comment: Commentaire ajouté par l'utilisateur à la création.
    @ivar start: Date de début de la mise en silence.
    @ivar end: Date de fin de la mise en silence.
    @ivar idstatus: Identifiant du statut de la mise en silence.
    @ivar status: Instance du statut de la mise en silence.
    """

    __tablename__ = bdd_basename + 'downtime'

    iddowntime = Column(
        Integer,
        primary_key=True, nullable=False, autoincrement=True
    )

    idsupitem = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'supitem.idsupitem',
            onupdate='CASCADE', ondelete='CASCADE',
        ),
        nullable=False,
    )

    supitem = relation('SupItem')

    entrytime = Column(DateTime(timezone=False), nullable=False)

    author = Column(
        Unicode(255),
        ForeignKey(
            bdd_basename + 'user.user_name',
            onupdate='CASCADE', ondelete='CASCADE',
        ),
        nullable=False,
    )

    user = relation('User')

    comment = Column(Text, nullable=True)
    
    start = Column(DateTime(timezone=False), nullable=False)
    
    end = Column(DateTime(timezone=False), nullable=False)

    idstatus = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'downtime_status.idstatus',
            onupdate='CASCADE', ondelete='CASCADE',
        ),
        nullable=False,
    )

    status = relation('DowntimeStatus')


    def __init__(self, **kwargs):
        """
        Initialisation.
        """
        super(Downtime, self).__init__(**kwargs)

