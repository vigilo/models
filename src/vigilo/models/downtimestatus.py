# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table DowntimeStatus"""
from sqlalchemy import Column
from sqlalchemy.orm import relation
from sqlalchemy.types import Text, DateTime, Integer, Unicode

from vigilo.models.configure import DeclarativeBase, DBSession, ForeignKey

__all__ = ('DowntimeStatus', )

class DowntimeStatus(DeclarativeBase, object):
    """
    Statuts possibles d'une opération de mise en silence.

    @ivar idstatus: Identifiant du statut.
    @ivar status: État de l'opération.
        Valeurs possibles : 'Scheduled', 'Active', 'Finished', 'Cancelled'.
    """

    __tablename__ = 'downtime_status'

    idstatus = Column(
        Integer,
        primary_key=True, nullable=False, autoincrement=True,
    )

    status = Column(
        Unicode(32),
        nullable=True,
    )

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
        
        @param cls: Classe à utiliser pour la requête.
        @type cls: C{DeclarativeBase}
        @param status_name: Nom du statut voulu.
        @type status_name: C{unicode}
        @return: L'identifiant du statut demandé.
        @rtype: C{int} ou None
        """
        return DBSession.query(cls.idstatus).filter(
            cls.status == status_name).scalar()

    @classmethod
    def value_to_status_name(cls, status_id):
        """
        Renvoie le nom du statut dont 
        l'identifiant est passé en paramètre.
        
        @param cls: Classe à utiliser pour la requête.
        @type cls: C{DeclarativeBase}
        @param status_id: L'identifiant du statut demandé.
        @type status_id: C{int}
        @return: Le nom du statut voulu.
        @rtype: C{unicode} ou None
        """
        return DBSession.query(cls.status).filter(
            cls.idstatus == status_id).scalar()

