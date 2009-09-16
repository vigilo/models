# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Host"""
from __future__ import absolute_import

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, UnicodeText
from sqlalchemy.orm import relation
from sqlalchemy.ext.associationproxy import association_proxy
from pylons.i18n import lazy_ugettext as l_

from .vigilo_bdd_config import bdd_basename, DeclarativeBase, metadata
from .session import DBSession

__all__ = ('Host', )

class Host(DeclarativeBase):
    __tablename__ = bdd_basename + 'host'

    name = Column(
        Unicode(255),
        index=True, primary_key=True, nullable=False)

    checkhostcmd = Column(
        UnicodeText,
        nullable=False)

    community = Column(
        Unicode(255),
        nullable=False)

    fqhn = Column(
        Unicode(255),
        nullable=False)

    hosttpl = Column(
        Unicode(255),
        nullable=False)

    mainip = Column(
        Unicode(15),
        nullable=False)

    port = Column(Integer, nullable=False)

    snmpoidsperpdu = Column(Integer)

    snmpversion = Column(Unicode(255))

    groups = association_proxy('host_groups', 'groups')


    def __init__(self, **kwargs):
        """Initialise un hôte."""
        DeclarativeBase.__init__(self, **kwargs)

    def __unicode__(self):
        """
        Formatte un C{Host} pour l'afficher dans les formulaires.

        Le nom de l'hôte est utilisé pour le représenter dans les formulaires.

        @return: Le nom de l'hôte.
        @rtype: C{str}
        """
        return self.name

    @classmethod
    def by_host_name(cls, hostname):
        """
        Renvoie l'hôte dont le nom est L{hostname}.
        
        @param hostname: Nom de l'hôte voulu.
        @type hostname: C{unicode}
        @return: L'hôte demandé.
        @rtype: L{Host}
        """
        return DBSession.query(cls).filter(cls.name == hostname).first()


# Rum metadata.
from rum import fields
from .tag import Tag

fields.FieldFactory.fields(
    Host, (
        fields.Unicode('name',
            searchable=True, sortable=True, required=True,
            label=l_('Hostname')),

        fields.UnicodeText('checkhostcmd',
            searchable=True, sortable=True, required=True,
            label=l_('Command to check host')),

        fields.Unicode('fqhn',
            searchable=True, sortable=True, required=True,
            label=l_('Fully qualified hostname')),

        fields.Unicode('hosttpl',
            searchable=True, sortable=True, required=True,
            label=l_('Template')),

        fields.Unicode('mainip',
            searchable=True, sortable=True, required=True,
            label=l_('Main IP address')),

        fields.Integer('port',
            searchable=True, sortable=True, required=True,
            range=range(0, 65535),
            label=l_('Port')),

        fields.Unicode('community',
            searchable=True, sortable=True, required=True,
            label=l_('SNMP community')),

        fields.Unicode('snmpversion',
            searchable=True, sortable=True,
            label=l_('SNMP version')),

        fields.Integer('snmpoidsperpdu',
            searchable=True, sortable=True,
            label=l_('SNMP OIDs per PDU')),

        fields.Collection('tags', other=Tag, remote_name='name',
            label=l_('Tags')),
    )
)

