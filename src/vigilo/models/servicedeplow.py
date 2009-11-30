# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table ServiceDepLowOnLow."""
from __future__ import absolute_import

from sqlalchemy import ForeignKey, Column
from sqlalchemy.orm import relation
from sqlalchemy.types import Unicode, Integer

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .service import ServiceLowLevel

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

    _idservice = Column(
        'idservice', Integer,
        ForeignKey(
            bdd_basename + 'servicelowlevel.idservice',
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        primary_key=True, autoincrement=False,
    )

    service = relation('ServiceLowLevel', foreign_keys=[_idservice],
                    primaryjoin='ServiceLowLevel.idsupitem == ' + \
                        'ServiceDepLowOnLow._idservice')

    _iddep = Column(
        'iddep', Integer,
        ForeignKey(
            bdd_basename + 'servicelowlevel.idservice',
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        primary_key=True, autoincrement=False,
    )

    service_dep = relation('ServiceLowLevel', foreign_keys=[_iddep],
                        primaryjoin='ServiceLowLevel.idsupitem == ' + \
                            'ServiceDepLowOnLow._iddep')

    def __init__(self, **kwargs):
        super(ServiceDepLowOnLow, self).__init__(**kwargs)

