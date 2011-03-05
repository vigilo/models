# -*- coding: utf-8 -*-
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

