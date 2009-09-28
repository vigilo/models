# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table HighLevelService."""
from __future__ import absolute_import

from sqlalchemy import ForeignKey, Column
from sqlalchemy.orm import relation
from sqlalchemy.types import Unicode, UnicodeText, Integer

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from vigilo.models.session import DBSession

__all__ = ('HighLevelService', )

from .highlevelservicedep import HighLevelServiceDep

class HighLevelService(DeclarativeBase, object):
    """
    Service de haut niveau.

    La classe L{HighLevelService} gère un service de haut niveau.
    Un service de haut niveau dépend d'autres services qui peuvent être de
    bas niveau (L{Service} technique) ou de haut niveau (autres instance de
    L{HighLevelService}). Les dépendances sont gérées via les classes
    L{HighLevelServiceDepLowLevel} et L{HighLevelServiceDepHighLevel}.

    @ivar servicename: Le nom du service de haut niveau.
    @ivar message: Le message à afficher dans Vigiboard lorsque le service
        passe dans un état autre que UP.
    @ivar seuil: Le seuil à partir duquel le service passe de l'état WARNING
        à l'état CRITICAL.
    @ivar op_dep: Le type d'opération à appliquer aux dépendances de ce
        service de haut niveau ('+', 'et' ou 'ou').
    @ivar dependancies: Liste des dépendances de ce service de haut niveau.
    @ivar higher_services: Liste des services de haut niveau qui dépendent
        du service de haut niveau courant.
    @ivar weight: Le poids affecté à ce nœud, calculé en fonction du type
        de l'opération pour les dépendances et du poids de ces différentes
        dépendances.
    """

    __tablename__ = bdd_basename + 'highlevelservice'

    hostname = Column(
        Unicode(255),
        ForeignKey(
            bdd_basename + u'host.name'
        ),
        primary_key=True, nullable=False)

    servicename = Column(
        Unicode(255),
        ForeignKey(
            bdd_basename + u'service.name'
        ),
        primary_key=True)

    message = Column(
        UnicodeText,
        nullable=False,
    )

    seuil = Column(
        Integer,
        nullable=False,
    )

    op_dep = Column(
        Unicode(2),
        nullable=False,
    )

    dependancies = relation('HighLevelServiceDep',
        primaryjoin= \
            hostname == HighLevelServiceDep.hostname and \
            servicename == HighLevelServiceDep.servicename,
        uselist=True)

    @property
    def weight(self):
        # Opération '+' : le poids vaut la somme des poids des dépendances.
        if self.op_dep == u'+':
            result = 0
            for dep in self.dependancies:
                result += dep.weight
            return result

        # Opération 'et': le poids vaut le minimum des poids des dépendances.
        if self.op_dep == u'et':
            if len(self.dependancies) == 0:
                return 0
            return min(self.dependancies, key=lambda x: x.weight).weight

        # Opération 'ou': le poids vaut le maximum des poids des dépendances.
        if self.op_dep == u'ou':
            if len(self.dependancies) == 0:
                return 0
            return max(self.dependancies, key=lambda x: x.weight).weight

        # Type d'opération inconnu.
        raise TypeError('Unknown dependancy operator "%s"' % op_dep)


    def __init__(self, **kwargs):
        DeclarativeBase.__init__(self, **kwargs)

    def __unicode__(self):
        """Représentation plus sympathique de l'objet."""
        return self.servicename

    @classmethod
    def by_host_service_name(cls, hostname, servicename):
        """
        Renvoie le L{HighLevelService} dont le nom d'hôte virtuel
        est L{hostname} et le nom de service virtuel est L{servicename}.
        
        @param hostname: Nom de l'hôte virtuel voulu.
        @type hostname: C{unicode}
        @param servicename: Nom du service virtuel voulu.
        @type servicename: C{unicode}
        @return: Le service demandé.
        @rtype: L{Service} ou None
        """
        return DBSession.query(cls).filter(cls.hostname == hostname) \
            .filter(cls.servicename == servicename).first()

    def get_error_message(self):
        """
        Renvoie le message à afficher lorsque le statut du service
        n'est pas UP.
        """
        # XXX Le message doit tenir compte des infos du service de bas niveau
        # impacté. Pour le moment, on renvoie un message simple.
        return self.message

