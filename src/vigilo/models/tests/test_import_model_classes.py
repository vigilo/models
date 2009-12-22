# -*- coding: utf-8 -*-
"""Teste l'import des classes du modèle."""
import nose

def test_import_model_classes():
    """
    Teste si un import * dans les classes du modèle fonctionne.

    Ceci permet de détecter des erreurs dans la définition
    de la variable spéciale __all__.
    """
    from vigilo.models import *

