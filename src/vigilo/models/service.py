# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Service"""
from __future__ import absolute_import

from sqlalchemy import Column
from sqlalchemy.types import UnicodeText, Unicode
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relation

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .session import DBSession
from .secondary_tables import SERVICE_TAG_TABLE

__all__ = ('Service', )

class Service(DeclarativeBase, object):
    """
    Service de bas niveau (service technique).
    
    @ivar name: Nom du service.
    @ivar servicetype: ???.
    @todo: documenter l'attribut servicetype.
    @ivar command: Commande à exécuter pour vérifier l'état du service.
    @ivar servicegrops: Liste des groupes de services auxquels
        ce service appartient.
    @ivar tags: Liste des libellés associés à ce service.
    @ivar dependancies: Liste des services dont ce service dépend.
        Pour les services techniques, cette liste est toujours vide.
    """

    __tablename__ = bdd_basename + 'service'

    name = Column(
        Unicode(255),
        index=True, primary_key=True, nullable=False)

    servicetype = Column(
        Unicode(255),
        default=u'0', nullable=False)

    command = Column(
        UnicodeText,
        default=u'', nullable=False)

    servicegroups = relation('ServiceGroup', back_populates='services', uselist=True, )

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

