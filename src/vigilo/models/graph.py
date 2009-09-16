# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Graph"""
from __future__ import absolute_import

from sqlalchemy import Column
from sqlalchemy.types import Unicode
from pylons.i18n import lazy_ugettext as l_

from .vigilo_bdd_config import bdd_basename, DeclarativeBase

__all__ = ('Graph', )

class Graph(DeclarativeBase, object):
    __tablename__ = bdd_basename + 'graph'

    name = Column(
        Unicode(255),
        primary_key=True, nullable=False)

    template = Column(
        Unicode(255),
        default=u'', nullable=False)

    vlabel = Column(
        Unicode(255),
        default=u'', nullable=False)


    def __init__(self, **kwargs):
        DeclarativeBase.__init__(self, **kwargs)

    def __unicode__(self):
        return self.name


# Rum metadata.
from rum import fields

fields.FieldFactory.fields(
    Graph, (
        fields.Unicode('name',
            searchable=True, sortable=True, required=True,
            label=l_('Graph name')),

        fields.Unicode('template',
            searchable=True, sortable=True, required=True,
            label=l_('Template')),

        fields.Unicode('vlabel',
            searchable=True, sortable=True, required=True,
            label=l_('Vertical label')),
    )
)

