# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Service"""
from __future__ import absolute_import

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.types import UnicodeText, Unicode
from sqlalchemy.orm import relation
from sqlalchemy.ext.associationproxy import association_proxy

from .vigilo_bdd_config import bdd_basename, DeclarativeBase, metadata
from .session import DBSession

__all__ = ('Service', )

class Service(DeclarativeBase):
    """
    Service de bas niveau (service technique).
    """

    __tablename__ = bdd_basename + 'service'

    name = Column(
        Unicode(255),
        index=True, primary_key=True, nullable=False)

    servicetype = Column(
        Unicode(255),
        default=u'0', nullable=False)

    command = Column(
        UnicodeText,
        default=u'', nullable=False)

    groups = association_proxy('service_groups', 'groups')

    @property
    def dependancies(self):
        return []



    def __init__(self, **kwargs):
        """Initialise un service."""
        DeclarativeBase.__init__(self, **kwargs)

    def __unicode__(self):
        """
        Formatte un C{Service} pour l'afficher dans les formulaires.

        Le nom du service est utilisé pour le représenter dans les formulaires.

        @return: Le nom du service.
        @rtype: C{str}
        """
        return self.name

    @classmethod
    def by_service_name(cls, servicename):
        """
        Renvoie le service dont le nom est L{servicename}.
        
        @param servicename: Nom du service voulu.
        @type servicename: C{unicode}
        @return: Le service demandé.
        @rtype: L{Service} ou None
        """
        return DBSession.query(cls).filter(cls.name == servicename).first()

