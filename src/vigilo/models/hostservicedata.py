# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table HostServiceData."""
from __future__ import absolute_import

from sqlalchemy import ForeignKey, Column
from sqlalchemy.orm import synonym
from sqlalchemy.types import Unicode, Integer

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from vigilo.models.session import DBSession

__all__ = ('HostServiceData', )

class HostServiceData(DeclarativeBase, object):
    """
    Associe des informations à un couple hôte/service.
    """

    __tablename__ = bdd_basename + 'hostservicedata'

    hostname = Column(
        Unicode(255),
        ForeignKey(
            bdd_basename + u'host.name',
            onupdate="CASCADE", ondelete="CASCADE",
        ),
        primary_key=True, nullable=False)

    servicename = Column(
        Unicode(255),
        ForeignKey(
            bdd_basename + u'service.name',
            onupdate="CASCADE", ondelete="CASCADE",
        ),
        primary_key=True)

    weight = Column(
        Integer,
        nullable=False,
    )

    _priority = Column(
        'priority', Integer,
        nullable=False,
    )

    def _get_priority(self):
        """Renvoie la priorité associée à un couple hôte/service."""
        return self._priority

    # XXX on devrait s'assurer que la priorité est bornée.
    # Ceci permettra aussi de définir les limites pour Rum (Vigicore).
    def _set_priority(self, priority):
        """Modifie la priorité associée à un couple hôte/service."""
        self._priority = priority

    priority = synonym('_priority',
        descriptor=property(_get_priority, _set_priority))


    def __init__(self, **kwargs):
        """Initialise les informations sur un couple hôte/service."""
        super(HostServiceData, self).__init__(**kwargs)

    @classmethod
    def by_host_service_name(cls, hostname, servicename):
        """
        Renvoie le service de haut niveau dont le nom d'hôte virtuel
        est L{hostname} et le nom de service virtuel est L{servicename}.
        
        @param hostname: Nom de l'hôte virtuel voulu.
        @type hostname: C{unicode}
        @param servicename: Nom du service virtuel voulu.
        @type servicename: C{unicode}
        @return: Le service demandé.
        @rtype: L{Service} ou None
        """
        return DBSession.query(cls).filter(cls.hostname == hostname) \
            .filter(cls.servicename == servicename).first()

