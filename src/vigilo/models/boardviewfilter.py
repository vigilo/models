# -*- coding: utf-8 -*-
"""Modèle pour la table BoardViewFilter."""
from __future__ import absolute_import

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Unicode, UnicodeText
from pylons.i18n import lazy_ugettext as l_

from vigilo.models.vigilo_bdd_config import bdd_basename, DeclarativeBase
from vigilo.models.session import DBSession

__all__ = ('BoardViewFilter', )

class BoardViewFilter(DeclarativeBase, object):
    """Gère les filtres personnalisés d'un utilisateur dans Vigiboard."""

    __tablename__ = bdd_basename + 'boardviewfilter'

    filtername = Column(
        Unicode(255),
        primary_key=True, index=True, nullable=False)

    username = Column(
        Unicode(255),
        ForeignKey(
            bdd_basename + 'user.user_name',
            onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True, index=True, nullable=False)

    hostname = Column(
        UnicodeText,
        ForeignKey(
            bdd_basename + 'host.name',
            onupdate="CASCADE", ondelete="CASCADE"),
        index=True, nullable=False)

    servicename = Column(
        UnicodeText,
        ForeignKey(
            bdd_basename + 'service.name',
            onupdate="CASCADE", ondelete="CASCADE"),
        index=True, nullable=False)

    message = Column(UnicodeText)

    trouble_ticket = Column(UnicodeText)

    def __init__(self, **kwargs):
        """Initialise un filtre."""
        DeclarativeBase.__init__(self, **kwargs)


# Rum metadata.
from rum import fields
from .service import Service
from .host import Host
from .user import User

fields.FieldFactory.fields(
    BoardViewFilter, (
        fields.Unicode('filtername',
            required=True, searchable=True, sortable=True,
            label=l_('Filter name')),

        fields.Relation('username', User, 'user_name',
            required=True, searchable=True, sortable=True,
            label=l_('Username')),

        fields.Relation('hostname', Host, 'name',
            required=True, searchable=True, sortable=True,
            label=l_('Hostname')),

        fields.Relation('servicename', Service, 'name',
            required=True, searchable=True, sortable=True,
            label=l_('Service name')),

        fields.UnicodeText('message',
            searchable=True, sortable=True,
            label=l_('Message')),

        fields.UnicodeText('trouble_ticket',
            searchable=True, sortable=True,
            label=l_('Trouble ticket')),
    )
)

