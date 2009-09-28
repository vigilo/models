# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table HighLevelServiceDep."""
from __future__ import absolute_import

from sqlalchemy import ForeignKey, Column
from sqlalchemy.orm import composite
from sqlalchemy.types import Unicode
from sqlalchemy.schema import ForeignKeyConstraint

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from vigilo.models.session import DBSession

from .service import Service
from .state import State
from .serviceweight import ServiceWeight

__all__ = ('HighLevelServiceDepHighLevel', 'HighLevelServiceDepLowLevel', )

class HighLevelServiceDep(DeclarativeBase, object):
    """
    Dépendance d'un service de haut niveau.

    La classe L{HighLevelServiceDep} est une base abstraite pour la gestion
    des dépendances d'un service de haut niveau.
    Une dépendance peut porter sur un service de bas niveau
    (L{Service} technique), auquel cas elle est gérée par la classe
    L{HighLevelServiceDepLowLevel}. Ou bien, elle peut porter sur un
    autre service de haut niveau (L{HighLevelService}). Dans ce cas,
    c'est la classe L{HighLevelServiceDepHighLevel} qui la gèrera.

    @ivar hostname: Le nom de l'hôte de haut niveau considéré.
    @ivar servicename: Le nom du service de haut niveau considéré.
    @ivar host_dep: Le nom de l'hôte de la dépendance.
    @ivar service_dep: Le nom du service de la dépendance.
    @ivar type_dep: Le type de dépendance ('lowlevel' ou 'highlevel').
    """
    __tablename__ = bdd_basename + 'highlevelservicedep'

    hostname = Column(
        Unicode(255),
        ForeignKey(bdd_basename +'highlevelservice.hostname'),
        primary_key=True, nullable=False,
    )

    servicename = Column(
        Unicode(255),
        ForeignKey(bdd_basename +'highlevelservice.servicename'),
        primary_key=True,
    )

    host_dep = Column(
        'hostname_dep',
        Unicode(255),
        index=True, primary_key=True, nullable=False,
    )

    service_dep = Column(
        'servicename_dep',
        Unicode(255),
        index=True, primary_key=True,
    )    

    type_dep = Column(
        'type_dep',
        Unicode(16),
        index=True, primary_key=True, nullable=False,
    )

    __mapper_args__ = { 'polymorphic_on': type_dep }

    def __init__(self, **kwargs):
        DeclarativeBase.__init__(self, **kwargs)

    @property
    def weight(self):
        raise RuntimeError('No weight attribute on abstract base class')


class HighLevelServiceDepHighLevel(HighLevelServiceDep):
    """
    Classe chargée de la gestion d'une dépendance entre deux services
    de haut niveau.

    @ivar weight: Le poids courant de la dépendance. Le calcul du poids tient
        compte de l'état actuel de la dépendance, de ses sous-dépendances,
        et récursivement.
    """

    __mapper_args__ = {'polymorphic_identity': u'highlevel'}

    @property
    def weight(self):
        # On calcule le poids de ce service de haut niveau
        # en fonction du poids de ses dépendances.
        return HighLevelService.by_host_service_name(
            hostname=self.host_dep, servicename=self.service_dep).weight

    def __init__(self, **kwargs):
        HighLevelServiceDep.__init__(self, **kwargs)
        self.type_dep = u'highlevel'

class HighLevelServiceDepLowLevel(HighLevelServiceDep):
    """
    Class chargée de la gestion de dépendances entre un service de haut niveau
    et un service de bas niveau (L{Service} technique).

    @ivar weight: Le poids courant de la dépendance. Le calcul du poids tient
        compte de l'état actuel de la dépendance, de ses sous-dépendances,
        et récursivement.
    """

    __mapper_args__ = {'polymorphic_identity': u'lowlevel'}

    @property
    def weight(self):
        # On cherche le dernier état de cet (hôte, service).
        last_state = DBSession.query(State) \
            .filter(State.hostname == self.host_dep) \
            .filter(State.servicename == self.service_dep) \
            .order_by(State.timestamp.desc()).first()

        # Si le dernier état n'est pas 'OK',
        # on considère que (hôte, service) est inopérant.
        if not last_state is None and last_state.statename != 'OK':
            return 0
        return ServiceWeight.by_host_service_name(
            hostname=self.host_dep, servicename=self.service_dep).weight

    def __init__(self, **kwargs):
        HighLevelServiceDep.__init__(self, **kwargs)
        self.type_dep = u'lowlevel'

