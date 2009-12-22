# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table HostApplication."""
from __future__ import absolute_import

from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Unicode, Integer
from sqlalchemy.orm import relation
from sqlalchemy.schema import UniqueConstraint

from .vigilo_bdd_config import bdd_basename, DeclarativeBase

__all__ = ('HostApplication', 'HostBusApplication')

class HostApplication(DeclarativeBase, object):
    """
    Liaison entre un hôte, un serveur d'applications de Vigilo
    et une application.
    
    @ivar idhost: Identifiant de l'hôte auquel est liée l'application.
    @ivar idappserver: Identifiant du serveur d'application associé.
    @ivar idapp: Identifiant de l'application.

    """
    __tablename__ = bdd_basename + 'hostapp'
    __table_args__ = (
        UniqueConstraint('idhost', 'idapp'),
        {}
    )

    idhost = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'host.idhost',
            onupdate='CASCADE', ondelete='CASCADE',
        ),
        primary_key=True,
        nullable=False,
        autoincrement=False,
    )

    host = relation('Host',
        primaryjoin='HostApplication.idhost == Host.idhost')

    idappserver = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'host.idhost',
            onupdate='CASCADE', ondelete='CASCADE',
        ),
        primary_key=True,
        nullable=False,
        autoincrement=False,
    )

    appserver = relation('Host',
        primaryjoin='HostApplication.idappserver == Host.idhost')

    idapp = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'application.idapp',
            onupdate='CASCADE', ondelete='CASCADE',
        ),
        primary_key=True,
        nullable=False,
        autoincrement=False,
    )

    application = relation('Application')

    __apptype = Column(
        'apptype', Unicode(16),
        nullable=True,
    )

    __mapper_args__ = {'polymorphic_on': __apptype}

    def __init__(self, **kwargs):
        """Initialise une instance de HostApplication."""
        super(HostApplication, self).__init__(**kwargs)


class HostBusApplication(HostApplication):
    """
    Liaison entre un hôte, un serveur d'applications de Vigilo
    et une application connectée au bus.
    """

    __mapper_args__  = {'polymorphic_identity': u'bus'}

    jid = Column(
        Unicode(255),
    )

    def __init__(self, **kwargs):
        """Initialise une instance de HostBusApplication."""
        if 'jid' not in kwargs:
            raise KeyError, 'Missing value for "jid" attribute.'
        super(HostBusApplication, self).__init__(**kwargs)

