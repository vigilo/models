# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2014 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèle pour la table EventsAggregate"""
from vigilo.models.session import DeclarativeBase
from vigilo.models.tables.secondary_tables import EVENTSAGGREGATE_TABLE

__all__ = ('EventsAggregate', )


class EventsAggregate(DeclarativeBase):
    """
    Classe servant d'enrobage autour de la table secondaire
    L{EVENTSAGGREGATE_TABLE}.
    """
    __table__ = EVENTSAGGREGATE_TABLE
