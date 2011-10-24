# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2011 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèle pour la table Tag"""
from sqlalchemy import Column
from sqlalchemy.types import Unicode, Integer
from sqlalchemy.orm import relation, synonym

from vigilo.models.session import DeclarativeBase, DBSession, ForeignKey

class Tag(DeclarativeBase, object):
    """
    Un tag associé soit à un élément supervisé.

    @ivar name: Nom du tag.
    @ivar value: Valeur associée au tag.
    @ivar supitems: Liste des éléments supervisés (L{SupItem}s) auxquels
        le tag est rattaché.
    """

    __tablename__ = 'tag'

    idsupitem = Column(
        Integer,
        ForeignKey(
            'supitem.idsupitem',
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
        autoincrement=False,
    )

    name = Column(
        Unicode(255),
        primary_key=True,
        index=True,
    )

    _value = Column(
        'value',
        Unicode(255),
        nullable=True,
    )

    supitem = relation('SupItem', lazy=True)

    def __get_value(self):
        return self._value

    def __set_value(self, value):
        if value is not None:
            value = unicode(value)
        self._value = value

    value = synonym("_value", map_column=True,
        descriptor=property(__get_value, __set_value))

    def __init__(self, name, value=None, **kwargs):
        """Initialise un tag."""
        if value is not None:
            value = unicode(value)
        super(Tag, self).__init__(name=unicode(name), value=value, **kwargs)

    def __unicode__(self):
        """
        Représentation unicode du tag.

        @return: Le nom du tag.
        @rtype: C{unicode}
        """
        return self.name

    @classmethod
    def by_supitem_and_tag_name(cls, supitem, tagname):
        """
        Récupère un tag par son nom.

        @param supitem: Instance sur laquelle porte le tag.
        @type: L{SupItem}
        @param tagname: Nom du tag à récupérer.
        @type tagname: C{unicode}
        @return: Instance du Tag.
        @rtype: L{Tag}
        """
        if not isinstance(supitem, int):
            supitem = supitem.idsupitem
        return DBSession.query(cls).filter(cls.name == unicode(tagname)
            ).filter(cls.idsupitem == supitem).first()
