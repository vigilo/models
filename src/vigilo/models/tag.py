# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Tag"""
from __future__ import absolute_import

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.types import Unicode
from sqlalchemy.orm import relation

from .vigilo_bdd_config import bdd_basename, DeclarativeBase, metadata

HOST_TAG_TABLE = Table(
    bdd_basename + 'tags2hosts', metadata,
    Column('hostname', Unicode(255), ForeignKey(
                bdd_basename + 'host.name',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
    Column('name', Unicode(255), ForeignKey(
                bdd_basename + 'tag.name',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True)
)

SERVICE_TAG_TABLE = Table(
    bdd_basename + 'tags2services', metadata,
    Column('servicename', Unicode(255), ForeignKey(
                bdd_basename + 'service.name',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
    Column('name', Unicode(255), ForeignKey(
                bdd_basename + 'tag.name',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True)
)


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
        backref='tags', lazy='dynamic')

    services = relation('Service', secondary=SERVICE_TAG_TABLE,
        backref='tags', lazy='dynamic')


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

