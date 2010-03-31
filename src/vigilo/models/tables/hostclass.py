# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table HostClass"""
from sqlalchemy import Column
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.orm import relation

from vigilo.models.session import DeclarativeBase, DBSession
from vigilo.models.tables.secondary_tables import HOST_HOSTCLASS_TABLE

__all__ = ('HostClass', )

class HostClass(DeclarativeBase, object):
    """
    Classe d'un hôte du parc informatique.

    Un hôte va pouvoir appartenir à plusieurs classes.
    Exemples de classes : "Solaris", "Solaris9", "net-snmp".
    Ces informations sont utilisées pour déterminer la meilleure
    stratégie à utiliser pour interroger l'équipement sur son état.

    @ivar idclass: Identifiant (auto-généré) de la classe.
    @ivar name: Le nom de la classe (ex: "Solaris").
    @ivar hosts: Liste des L{Host}s auxquels la classe d'hôte courante
        est attachée.
    """
    __tablename__ = 'hostclass'

    idclass = Column(
        Integer,
        primary_key=True, autoincrement=True,
    )

    name = Column(
        Unicode(255),
        unique=True, index=True, nullable=False,
    )

    hosts = relation('Host', secondary=HOST_HOSTCLASS_TABLE,
        back_populates='hostclasses', lazy=True)

    def __init__(self, **kwargs):
        """Initialise une classe d'hôtes."""
        super(HostClass, self).__init__(**kwargs)

    def __unicode__(self):
        """Renvoie la représentation unicode de la classe d'hôtes."""
        return self.name

    @classmethod
    def by_class_name(cls, classname):
        """Renvoie l'instance de L{HostClass} dont le nom est C{classname}."""
        DBSession.query(cls).filter(cls.name == classname).first()

