# -*- coding: utf-8 -*-
"""
Modèle de la base de données de Vigilo.
Contient les fichiers nécessaires à la configuration de la base de données,
sa création, son entretien et son utilisation.
"""

__all__ = (
    'VIGILO_MODELS_VERSION',
)

# Numéro de version du modèle, il sera incrémenté pour chaque nouvelle
# version livrée au client. Il sera utilisé par les scripts de mise à jour
# de Vigilo afin d'importer les données d'une ancienne version du modèle
# vers la nouvelle version (permet d'assurer la rétro-compatibilité).
VIGILO_MODELS_VERSION = 1

