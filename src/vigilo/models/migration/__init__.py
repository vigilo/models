# -*- coding: utf-8 -*-
# Copyright (C) 2006-2015 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Scripts de migration de la base de données.
Lors d'un changement dans le modèle, il faut rédiger un script de migration
dans ce dossier (numéroté) et mettre à jour les tables en elles-même (dans
le module L{vigilo.models.tables}).
Il faut également mettre à jour le compteur de version situé dans le module
L{vigilo.models.websetup}.
"""

# Note : les scripts de migration modifient parfois la structure (schéma)
# de la base de données. Dans ces cas là, la modification doit également
# être propagée via la réplication.
# Pour PostgreSQL, la réplication se fait en utilisant Slony qui utilise
# le concept d'ensembles (sets) pour regrouper les choses à répliquer
# et de nœuds pour désigner les machines vers lesquelles on réplique.
#
# Dans le modèle de réplication de Vigilo pour Slony, les nœuds sont
# définis de la façon suivante :
# - le nœud 1 correspond au nœud principal (maître),
# - le nœud 2 correspond au site de dévolution (esclave),
# - le nœud 3 correspond à VigiReport.
# La numérotation des ensembles suit celle des nœuds :
# - le set 2 correspond aux éléments répliqués pour la dévolution,
# - le set 3 correspond aux éléments répliqués vers VigiReport.
