# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table ServiceWeight."""
from __future__ import absolute_import

from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Unicode, Integer

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from vigilo.models.session import DBSession

__all__ = ('ServiceWeight', )

class ServiceWeight(DeclarativeBase, object):
    """
    Associe des informations à un couple hôte/service.
    """

    __tablename__ = bdd_basename + 'serviceweight'

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

    def __init__(self, **kwargs):
        super(ServiceWeight, self).__init__(**kwargs)

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

