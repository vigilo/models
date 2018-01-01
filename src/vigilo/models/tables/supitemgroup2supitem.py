# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2018 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèle pour la table SupItemGroup2SupItem"""
from vigilo.models.session import DeclarativeBase
from vigilo.models.tables.secondary_tables import SUPITEM_GROUP_TABLE

__all__ = ('SupItemGroup2SupItem', )


class SupItemGroup2SupItem(DeclarativeBase):
    """
    Classe servant d'enrobage autour de la table secondaire
    L{SUPITEM_GROUP_TABLE}.
    """
    __table__ = SUPITEM_GROUP_TABLE
