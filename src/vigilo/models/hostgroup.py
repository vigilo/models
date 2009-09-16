# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table HostGroup"""
from __future__ import absolute_import

from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Unicode
from sqlalchemy.orm import relation
from pylons.i18n import lazy_ugettext as l_

from .vigilo_bdd_config import bdd_basename, DeclarativeBase

__all__ = ('HostGroup', )

class HostGroup(DeclarativeBase, object):

    __tablename__ = bdd_basename + 'hostgroup'

    hostname = Column(
        Unicode(255),
        ForeignKey(bdd_basename + u'host.name'),
        primary_key=True, nullable=False)

    groupname = Column(
        Unicode(255),
        ForeignKey(bdd_basename + u'group.name'),
        primary_key=True, nullable=False)

#    host = relation('Host', backref='host_groups')
#    group = relation('Group', backref='hosts')

    def __init__(self, **kwargs):
        """Initialise un groupe d'hôtes."""
        DeclarativeBase.__init__(self, **kwargs)

    def __unicode__(self):
        return u'%s - %s' % (self.groupname, self.hostname)


# Rum metadata.
from rum import fields
from .host import Host
from .group import Group

fields.FieldFactory.fields(
    HostGroup, (
        fields.Relation('groupname', Group, 'name',
            required=True, searchable=True, sortable=True,
            label=l_('Group name')),

        fields.Relation('hostname', Host, 'name',
            required=True, searchable=True, sortable=True,
            label=l_('Hostname')),
    )
)

