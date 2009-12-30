# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Downtime"""
from __future__ import absolute_import

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relation
from sqlalchemy.types import Text, DateTime, Integer, String

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .session import DBSession

__all__ = ('Downtime', 'DowntimeStatus',)


class DowntimeStatus(DeclarativeBase, object):
    """
    Statuts possibles d'une opération de mise en silence.

    @ivar iddowntimestatus: Identifiant du statut.
    @ivar status: Etat de l'opération.
    """

    __tablename__ = bdd_basename + 'downtime_status'

    # Colonne idstatus
    idstatus = Column(
        Integer,
        primary_key=True, nullable=False, autoincrement=True
    )

    # Colonne status
    status = Column(String, nullable=True)


    def __init__(self, **kwargs):
        """
        Initialisation.
        """
        super(DowntimeStatus, self).__init__(**kwargs)

    @classmethod
    def status_name_to_value(cls, status_name):
        """
        Renvoie l'identifiant du statut de mise en 
        silence dont le nom est passé en paramètre.
        
        @param servicename: Nom du statut voulu.
        @type servicename: C{unicode}
        @return: L'identifiant du statut demandé.
        @rtype: C{int} ou None
        """
        status = DBSession.query(cls.idstatus).filter(
            cls.status == status_name).first()
        if status:
            return status.idstatus
        return None

    @classmethod
    def value_to_status_name(cls, status_id):
        """
        Renvoie le nom du statut dont 
        l'identifiant est passé en paramètre.
        
        @param: L'identifiant du statut demandé.
        @rtype: C{int}
        @return servicename: Le nom du statut voulu.
        @type servicename: C{unicode} ou None
        """
        status = DBSession.query(cls.status).filter(
            cls.idstatus == status_id).first()
        if status:
            return status.status
        return None


class Downtime(DeclarativeBase, object):
    """
    Mise en silence durant une maintenance.

    @ivar iddowntime: Identifiant de la mise en maintenance.
    @ivar idsupitem: Identifiant de l'item (hôte ou service) 
    mis en maintenance.
    @ivar entrytime: Date d'ajout de la mise en maintenance dans Vigilo.
    @ivar author: Utilisateur ayant créé cette mise en maintenance 
    dans Vigilo.
    @ivar comment: Commentaire ajouté par l'utilisateur à la création.
    @ivar start: Date de début de la mise en silence.
    @ivar end: Date de fin de la mise en silence.
    @ivar status: Statut de la mise en silence (valeurs possibles :
    'Planified', 'Enabled', 'Finished', 'Cancelled').
    """

    __tablename__ = bdd_basename + 'downtime'

    # Colonne iddowntime
    iddowntime = Column(
        Integer,
        primary_key=True, nullable=False, autoincrement=True
    )

    # Colonne idsupitem
    idsupitem = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'supitem.idsupitem',
            onupdate='CASCADE', ondelete='CASCADE',
        ),
        nullable=False,
    )

    supitem = relation('SupItem')

    # Colonne entrytime
    entrytime = Column(DateTime(timezone=False), nullable=False)

    # Colonne author
    author = Column(
        String,
        ForeignKey(
            bdd_basename + 'user.user_name',
            onupdate='CASCADE', ondelete='CASCADE',
        ),
        nullable=False,
    )

    user = relation('User')

    # Colonne comment
    comment = Column(Text, nullable=True)
    
    # Colonne start
    start = Column(DateTime(timezone=False), nullable=False)
    
    # Colonne end
    end = Column(DateTime(timezone=False), nullable=False)

    # Colonne status
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

