# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Tag"""
from sqlalchemy import Column
from sqlalchemy.types import Unicode
from sqlalchemy.orm import relation

from vigilo.models.configure import db_basename, DeclarativeBase
from vigilo.models.secondary_tables import SUPITEM_TAG_TABLE

class Tag(DeclarativeBase, object):
    """
    Un tag associé soit à un élément supervisé.
    
    @ivar name: Nom du tag.
    @ivar value: Valeur associée au tag.
    @ivar supitems: Liste des éléments supervisés (L{SupItem}s) auxquels
        le tag est rattaché.
    """

    __tablename__ = db_basename + 'tag'

    name = Column(
        Unicode(255),
        primary_key=True, index=True)

    value = Column(Unicode(255), nullable=True)

    supitems = relation('SupItem', secondary=SUPITEM_TAG_TABLE,
        back_populates='tags', lazy=True)


    def __init__(self, **kwargs):
        """Initialise un tag."""
        super(Tag, self).__init__(**kwargs)

    def __unicode__(self):
        """
        Représentation unicode du tag.
        
        @return: Le nom du tag.
        @rtype: C{unicode}
        """
        return self.name

