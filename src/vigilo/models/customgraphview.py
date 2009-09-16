# -*- coding: utf-8 -*-
"""Modèle pour la table CustomGraphView."""
from __future__ import absolute_import

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Unicode, Integer
from sqlalchemy.orm import relation
from pylons.i18n import lazy_ugettext as l_

from vigilo.models.vigilo_bdd_config import bdd_basename, DeclarativeBase
from vigilo.models.session import DBSession

__all__ = ('CustomGraphView', )

class CustomGraphView(DeclarativeBase, object):
    """Gère les vues personnalisées d'un utilisateur dans Vigigraph."""

    __tablename__ = bdd_basename + 'customgraphview'

    viewname = Column(
        Unicode(255),
        primary_key=True)

    username = Column(
        Unicode(255),
        ForeignKey(
            bdd_basename + 'user.user_name',
            onupdate="CASCADE", ondelete="CASCADE"),
        index=True, nullable=False, primary_key=True)

    graphname = Column(
        Unicode(255),
        ForeignKey(
            bdd_basename + 'graph.name',
            onupdate="CASCADE", ondelete="CASCADE"),
        index=True, nullable=False, primary_key=True)

    hostname = Column(
        Unicode(255),
        ForeignKey(
            bdd_basename + 'host.name',
            onupdate="CASCADE", ondelete="CASCADE"),
        index=True, nullable=False, primary_key=True)

    pos_x = Column(
        Integer,
        nullable=False)

    pos_y = Column(
        Integer,
        nullable=False)

    def __init__(self, **kwargs):
        """Initialise une vue."""   
        DeclarativeBase.__init__(self, **kwargs)


# Rum metadata.
from rum import fields
from .graph import Graph
from .host import Host
from .user import User

fields.FieldFactory.fields(
    CustomGraphView, (
        fields.Unicode('viewname',
            searchable=True, sortable=True, required=True,
            label=l_('View name')),

        fields.Relation('username', User, 'user_name',
            required=True, searchable=True, sortable=True,
            label=l_('Username')),

        fields.Relation('graphname', Graph, 'name',
            required=True, searchable=True, sortable=True,
            label=l_('Graph name')),

        fields.Relation('hostname', Host, 'name',
            required=True, searchable=True, sortable=True,
            label=l_('Hostname')),

        fields.Number('pos_x',
            required=True, range=(0, None),
            label='X'),

        fields.Number('pos_y',
            required=True, range=(0, None),
            label='Y'),
    )
)

