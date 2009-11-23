# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table PerfDataSource"""
from __future__ import absolute_import

from sqlalchemy import ForeignKey, Column
from sqlalchemy.orm import relation
from sqlalchemy.types import Integer, UnicodeText, Float

from .vigilo_bdd_config import bdd_basename, DeclarativeBase

__all__ = ('PerfDataSource', )

class PerfDataSource(DeclarativeBase, object):

    __tablename__ = bdd_basename + 'perfdatasource'

    idperfdatasource = Column(
        Integer,
        primary_key=True, autoincrement=True,
    )

    _idservice = Column(
        'idservice', Integer,
        ForeignKey(
            bdd_basename + 'servicelowlevel.idservice',
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        nullable=False,
    )

    service = relation('ServiceLowLevel')

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

