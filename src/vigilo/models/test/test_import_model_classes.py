# -*- coding: utf-8 -*-
# Copyright (C) 2011-2012 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Teste l'import des classes du modèle."""

def test_import_model_classes():
    """
    Teste si un import * dans les classes du modèle fonctionnerait.

    Ceci permet de détecter des erreurs dans la définition
    de la variable spéciale __all__.
    """
    from vigilo.models import tables
    for table in tables.__all__:
        getattr(tables, table)

