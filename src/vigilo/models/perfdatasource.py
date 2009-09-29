# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table PerfDataSource"""
from __future__ import absolute_import

from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Unicode, UnicodeText, Float

from .vigilo_bdd_config import bdd_basename, DeclarativeBase

__all__ = ('PerfDataSource', )

class PerfDataSource(DeclarativeBase, object):

    __tablename__ = bdd_basename + 'perfdatasource'

    hostname = Column(
        Unicode(255),
        ForeignKey(bdd_basename + u'host.name'),
        primary_key=True, nullable=False)

    servicename = Column(
        Unicode(255),
        ForeignKey(bdd_basename + u'service.name'),
        index=True, primary_key=True, nullable=False)

    graphname = Column(
        Unicode(255),
        ForeignKey(bdd_basename + u'graph.name'),
        index=True, nullable=False)

    type = Column(
        UnicodeText,
        default=u'', nullable=False)

    label = Column(
        UnicodeText,
        default=u'')

    factor = Column(
        Float(precision=None, asdecimal=False),
        default=0.0, nullable=False)

    def __init__(self, **kwargs):
        super(PerfDataSource, self).__init__(**kwargs)

