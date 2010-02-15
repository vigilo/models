# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table ConfItem"""
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Unicode, Integer
from sqlalchemy.orm import relation

from vigilo.models.supitem import SupItem

from vigilo.models.configure import DeclarativeBase

class ConfItem(DeclarativeBase, object):
    """
    Un confitem est associé à un élément supervisé.
    
    Typiquement utilisé pour associer une directive nagios
    à un hote ou un service de bas niveau.
    
    @ivar name: Nom du confitem.
    @ivar value: Valeur associée au confitem.
    @ivar supitem: élément supervisé (C{SupItem}) auxquel
        le confitem est rattaché.
    """

    __tablename__ = 'confitem'

    idconfitem = Column(
        Integer,
        primary_key=True, 
        autoincrement=True,
    )

    name = Column(Unicode(50), nullable=False)

    value = Column(Unicode(100), nullable=False)


    idsupitem = Column(
        Integer,
        ForeignKey(
            SupItem.idsupitem,
            onupdate='CASCADE', ondelete='CASCADE',
        ),
        nullable=False,
    )

    supitem = relation('SupItem')

    def __init__(self, **kwargs):
        """Initialise un confitem."""
        super(ConfItem, self).__init__(**kwargs)

    def __unicode__(self):
        """
        Représentation unicode du confitem.
        
        @return: Le nom du confitem.
        @rtype: C{unicode}
        """
        return self.name

