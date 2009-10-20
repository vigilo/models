# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Tag"""
from __future__ import absolute_import

from sqlalchemy import Column
from sqlalchemy.types import Unicode
from sqlalchemy.orm import relation

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .secondary_tables import HOST_TAG_TABLE, SERVICE_TAG_TABLE

class Tag(DeclarativeBase, object):
    """
    Un tag associé soit à un hôte, soit à un service.
    
    @ival content: Contenu du tag.
    @ival hosts: Liste des hôtes auxquels ce tag est associé.
    @ival services: Liste des services auxquels ce tag est associé.
    """

    __tablename__ = bdd_basename + 'tag'

    name = Column(
        Unicode(255),
        primary_key=True, index=True)

    value = Column(
        Unicode(255),
        unique=True, nullable=False, index=True)

    hosts = relation('Host', secondary=HOST_TAG_TABLE,
        back_populates='tags', lazy='dynamic')

    services = relation('Service', secondary=SERVICE_TAG_TABLE,
        back_populates='tags', lazy='dynamic')


    def __init__(self, **kwargs):
        """Initialise un tag."""
        super(Tag, self).__init__(**kwargs)

    def __unicode__(self):
        """
        Représentation unicode du tag.
        
        @return: Le contenu du tag.
        @rtype: C{unicode}
        """
        return self.content

