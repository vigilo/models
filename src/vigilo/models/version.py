# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Version"""
from sqlalchemy import Column
from sqlalchemy.types import Unicode, Integer

from vigilo.models.vigilo_bdd_config import bdd_basename, DeclarativeBase
from vigilo.models.session import DBSession

__all__ = ('Version', )

class Version(DeclarativeBase, object):
    """Stocke des informations sur la version d'un composant de Vigilo."""
    __tablename__ = bdd_basename + 'version'

    name = Column(
        Unicode(64),
        index=True,
        primary_key=True,
        nullable=False,
    )
    version = Column(
        Integer,
        nullable=False,
    )

    def __init__(self, **kwargs):
        """Initialise une instance de la classe Version."""
        super(Version, self).__init__(**kwargs)

    @classmethod
    def by_object_name(cls, object_name):
        return DBSession.query(cls).filter(cls.name == object_name).first()

