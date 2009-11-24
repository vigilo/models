# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour les tables ServiceDepHigh*."""
from __future__ import absolute_import

from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Unicode, Integer
from sqlalchemy.orm import relation

from .vigilo_bdd_config import bdd_basename, DeclarativeBase

__all__ = ('ServiceDepHighOnHigh', 'ServiceDepHighOnLow', )

class ServiceDepHigh(DeclarativeBase, object):
    """
    Dépendance d'un service de haut niveau.

    La classe L{ServiceDep} est une base abstraite pour la gestion
    des dépendances d'un service de haut niveau.
    Une dépendance peut porter sur un service de bas niveau
    (L{Service} technique), auquel cas elle est gérée par la classe
    L{ServiceDepLowLevel}. Ou bien, elle peut porter sur un
    autre service de haut niveau (L{HighLevelService}). Dans ce cas,
    c'est la classe L{ServiceDepHighLevel} qui la gère.

    @ivar _iddep: Identifiant autogénéré de la dépendance.
    @ivar servicename: Nom du service de haut niveau considéré.
    @ivar type_dep: Type de dépendance ('lowlevel' ou 'highlevel').
    """
    __tablename__ = bdd_basename + 'servicedephigh'

    _iddep = Column(
        'iddep', Integer,
        autoincrement=True, primary_key=True,
        unique=True,
    )

    _idservice = Column(
        'idservice', Integer,
        ForeignKey(
            bdd_basename + 'service.idservice',
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        nullable=False,
    )

    service = relation('Service')

    type_dep = Column(
        Unicode(16),
        nullable=False,
    )

    __mapper_args__ = {'polymorphic_on': type_dep}


    def __init__(self, **kwargs):
        super(ServiceDepHigh, self).__init__(**kwargs)


class ServiceDepHighOnHigh(ServiceDepHigh):
    """
    Classe chargée de la gestion d'une dépendance entre deux services
    de haut niveau.

    @ivar _iddep: Référence vers l'entrée correspondante dans la classe
        ServiceDep.
    @ivar service_dep: Nom du service de haut niveau dont ce service dépend.
    @ivar weight: Poids courant de la dépendance. Le calcul du poids tient
        compte de l'état actuel de la dépendance, de ses sous-dépendances, etc.
    """

    __tablename__ = bdd_basename + 'servicedephighonhigh'
    __mapper_args__ = {'polymorphic_identity': u'highlevel'}

    _iddep = Column(
        'iddep', Integer,
        ForeignKey(
            bdd_basename + 'servicedephigh.iddep',
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        primary_key=True,
    )

    _idservice_dep = Column(
        'idservice_dep', Integer,
        ForeignKey(
            bdd_basename + 'service.idservice',
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        index=True, nullable=False,
    )

    service_dep = relation('Service', foreign_keys=[_idservice_dep])

    def __init__(self, **kwargs):
        super(ServiceDepHighOnHigh, self).__init__(**kwargs)


class ServiceDepHighOnLow(ServiceDepHigh):
    """
    Classe chargée de la gestion de dépendances entre un service de haut niveau
    et un service de bas niveau (L{Service} technique).

    @ivar _iddep: Référence vers l'entrée correspondante dans la classe
        ServiceDep.
    @ivar host_dep: Nom d'hôte physique dont ce service dépend.
    @ivar weight: Poids courant de la dépendance. Le calcul du poids tient
    @ivar service_dep: Nom du service technique dont ce service dépend.
        compte de l'état actuel de la dépendance, de ses sous-dépendances, etc.
    """

    __tablename__ = bdd_basename + 'servicedephighonlow'
    __mapper_args__ = {'polymorphic_identity': u'lowlevel'}

    _iddep = Column(
        'iddep', Integer,
        ForeignKey(
            bdd_basename + 'servicedephigh.iddep',
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        primary_key=True,
    )

    _iddepservice = Column(
        'iddepservice', Integer,
        ForeignKey(
            bdd_basename + 'servicelowlevel.idservice',
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        nullable=False,
    )

    service_dep = relation('ServiceLowLevel')

    def __init__(self, **kwargs):
        super(ServiceDepHighOnLow, self).__init__(**kwargs)

