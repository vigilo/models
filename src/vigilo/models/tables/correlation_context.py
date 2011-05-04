# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2011 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèle pour la table CorrelationContext."""
from sqlalchemy import Column
from sqlalchemy.types import String, Text, DateTime

from vigilo.models.session import DeclarativeBase

__all__ = ('CorrelationContext', )

class CorrelationContext(DeclarativeBase):
    __tablename__ = 'correlation_context'

    key = Column(
            String(256),
            primary_key=True,
            index=True,
        )

    value = Column(
            Text,
            nullable=False,
        )

    expiration_date = Column(
            DateTime(timezone=False),
            nullable=True,
        )
