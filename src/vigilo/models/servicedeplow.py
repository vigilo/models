# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table ServiceDepLowOnLow."""
from __future__ import absolute_import

from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Unicode

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from vigilo.models.session import DBSession

from .state import State
from .hostservicedata import HostServiceData

__all__ = ('ServiceDepLowOnLow', )

class ServiceDepLowOnLow(DeclarativeBase, object):
    """
    Dépendance d'un service de bas niveau sur un autre.

    La classe L{ServiceDepLowOnLow} enregistre la dépendance d'un service
    de bas niveau sur un autre service de bas niveau.

    @ivar _iddep: Identifiant autogénéré de la dépendance.
    @ivar servicename: Nom du service de haut niveau considéré.
    @ivar type_dep: Type de dépendance ('lowlevel' ou 'highlevel').
    """
    __tablename__ = bdd_basename + 'servicedeplowonlow'

    hostname = Column(
        Unicode(255),
        ForeignKey(
            bdd_basename + 'host.name',
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        primary_key=True, nullable=True,
    )

    servicename = Column(
        Unicode(255),
        ForeignKey(
            bdd_basename + 'service.name',
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        primary_key=True, nullable=False,
    )

    host_dep = Column(
        Unicode(255),
        ForeignKey(
            bdd_basename + 'host.name',
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        index=True, nullable=False,
    )

    service_dep = Column(
        Unicode(255),
        ForeignKey(
            bdd_basename + 'service.name',
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        index=True, nullable=False,
    )    

    def __init__(self, **kwargs):
        super(ServiceDepLowOnLow, self).__init__(**kwargs)

