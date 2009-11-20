# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Service"""
from __future__ import absolute_import

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import UnicodeText, Unicode, Integer
from sqlalchemy.orm import relation

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .session import DBSession
from .secondary_tables import SERVICE_TAG_TABLE

__all__ = ('Service', )

class Service(DeclarativeBase, object):
    """
    Service générique.
    
    @ivar name: Nom du service.
    @ivar op_dep: Le type d'opération à appliquer aux dépendances de ce
        service de haut niveau ('+', '&' ou '|').
    @ivar servicetype: Indique le type de service. Vaut soit 'highlevel' pour
        un L{ServiceHighLevel}, soit 'lowlevel' pour un L{ServiceLowLevel}.
    @ivar servicegroups: Liste des groupes de services auxquels
        ce service appartient.
    @ivar tags: Liste des libellés associés à ce service.
    @ivar dependancies: Liste des services dont ce service dépend.
        Pour les services techniques, cette liste est toujours vide.
    """

    __tablename__ = bdd_basename + 'service'

    _idservice = Column(
        'idservice', Integer,
        autoincrement=True, primary_key=True,
    )

    name = Column(
        Unicode(255),
        index=True, unique=True, nullable=False,
    )

    op_dep = Column(
        Unicode(1),
        nullable=False,
    )

    _servicetype = Column(
        'servicetype', Unicode(16),
        nullable=False,
    )

    servicegroups = relation('ServiceGroup',
        back_populates='services', uselist=True, )

#    groups = association_proxy('servicegroups', 'groups')

    tags = relation('Tag', secondary=SERVICE_TAG_TABLE,
        back_populates='services', lazy='dynamic')

    # TODO: le service n'est pas lie a un hote ? Il devrait... (relation n-n)

    @property
    def dependancies(self):
        """
        Renvoie la liste des dépendances de ce service.

        Pour un L{Service} technique (de bas niveau), il n'y a jamais de
        dépendances, donc cette méthode renvoie une liste vide.
        Cette méthode existe afin de permettre d'appeler C{obj.dependancies}
        sur un service quelconque (de bas ou de haut niveau) sans provoquer
        d'erreurs.
        """
        return []

    __mapper_args__ = {'polymorphic_on': _servicetype}


    def __init__(self, **kwargs):
        """Initialise un service."""
        super(Service, self).__init__(**kwargs)

    def __unicode__(self):
        """
        Formatte un C{Service} pour l'afficher dans les formulaires.

        Le nom du service est utilisé pour le représenter dans les formulaires.

        @return: Le nom du service.
        @rtype: C{str}
        """
        return self.name

    @classmethod
    def by_service_name(cls, servicename):
        """
        Renvoie le service dont le nom est L{servicename}.
        
        @param servicename: Nom du service voulu.
        @type servicename: C{unicode}
        @return: Le service demandé.
        @rtype: L{Service} ou None
        """
        return DBSession.query(cls).filter(cls.name == servicename).first()


class ServiceLowLevel(Service):
    """
    Service de bas niveau (service technique).

    @ivar command: Commande à exécuter pour vérifier l'état du service.
    """
    __tablename__ = bdd_basename + 'servicelowlevel'
    __mapper_args__ = {'polymorphic_identity': u'lowlevel'}

    _idservice = Column(
        'idservice', Integer,
        ForeignKey(
            bdd_basename + 'service.idservice',
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        autoincrement=False, primary_key=True,
    )

    command = Column(
        UnicodeText,
        default=u'', nullable=False,
    )

    def __init__(self, **kwargs):
        super(ServiceLowLevel, self).__init__(**kwargs)


class ServiceHighLevel(Service):
    """
    Service de haut niveau.

    @ivar message: Message à afficher dans Vigiboard lorsque le service
        passe dans un état autre que OK.
    @ivar warning_threshold: Seuil à partir duquel le service passe de
        l'état OK à l'état WARNING.
    @ivar critical_threshold: Seuil à partir duquel le service passe de
        l'état WARNING à l'état CRITICAL.
    """
    __tablename__ = bdd_basename + 'servicehighlevel'
    __mapper_args__ = {'polymorphic_identity': u'highlevel'}

    _idservice = Column(
        'idservice', Integer,
        ForeignKey(
            bdd_basename + 'service.idservice',
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        autoincrement=False, primary_key=True,
    )

    message = Column(
        UnicodeText,
        nullable=False,
    )

    warning_threshold = Column(
        Integer,
        nullable=False,
    )

    critical_threshold = Column(
        Integer,
        nullable=False,
    )

    weight = Column(
        Integer,
        nullable=True,
    )

    def __init__(self, **kwargs):
        super(ServiceHighLevel, self).__init__(**kwargs)

