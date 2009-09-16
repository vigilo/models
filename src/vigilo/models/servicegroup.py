# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table ServiceGroup"""
from __future__ import absolute_import

from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Unicode
from sqlalchemy.orm import relation
from pylons.i18n import lazy_ugettext as l_

from .vigilo_bdd_config import bdd_basename, DeclarativeBase

__all__ = ('ServiceGroup', )

class ServiceGroup(DeclarativeBase, object):

    __tablename__ = bdd_basename + 'servicegroup'

    servicename = Column(
        Unicode(255),
        ForeignKey(bdd_basename + u'service.name'),
        primary_key=True, nullable=False)

    groupname = Column(
        Unicode(255),
        ForeignKey(bdd_basename + u'group.name'),
        primary_key=True, nullable=False)

#    service = relation('Service', backref='service_groups')
#    group = relation('Group', backref='services')

    def __init__(self, **kwargs):
        """Initialise un groupe de services."""
        DeclarativeBase.__init__(self, **kwargs)

    def __unicode__(self):
        return u'%s - %s' % (self.groupname, self.servicename)


# Rum metadata.
from rum import fields
from .service import Service
from .group import Group

fields.FieldFactory.fields(
    ServiceGroup, (
        fields.Relation('groupname', Group, 'groupname',
            required=True, searchable=True, sortable=True,
            label=l_('Group name')),

        fields.Relation('servicename', Service, 'servicename',
            required=True, searchable=True, sortable=True,
            label=l_('Service name')),
    )
)

