# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2011 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèle pour la table ConfFile"""
from sqlalchemy import Column
from sqlalchemy.types import Unicode, Integer
from sqlalchemy.orm import relation

from vigilo.models.session import DeclarativeBase, DBSession

class ConfFile(DeclarativeBase, object):
    """
    Cette table contient une entrée par fichier de configuration de VigiConf.
    Elle permet ensuite de déterminer rapidement dans quel fichier un élément
    du parc est configuré.

    @ivar idconffile: Identifiant unique du fichier de configuration.
    @ivar name: Nom (unique) du fichier de configuration,
        relatif au répertoire de base de la configuration de VigiConf.
    """

    __tablename__ = 'conffile'

    idconffile = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name = Column(
        Unicode(512),
        nullable=False,
        index=True,
        unique=True,
    )

    hosts = relation('Host', back_populates="conffile", cascade="all",
                     lazy=True)


    def __init__(self, **kwargs):
        """Initialise un ConfFile."""
        super(ConfFile, self).__init__(**kwargs)

    @classmethod
    def by_filename(cls, filename):
        """
        Renvoie l'instance correspondant au fichier de configuration
        dont le nom est passé.

        @param filename: Nom du fichier de configuration.
        @type  filename: C{unicode}
        @return: Instance correspondant à ce fichier de configuration
            s'il en existe une.
        @rtype: L{ConfFile} ou None
        """
        return DBSession.query(cls).filter(cls.name == filename).first()

    @classmethod
    def get_or_create(cls, filename):
        """
        Retourne une instance correspondant au fichier donné,
        en la créant si aucune instance n'existe.

        @param cls: Classe à utiliser.
        @type cls: L{ConfFile}
        @param filename: Nom du fichier de configuration.
        @type filename: C{basestring}
        @return: Instance correspondant au fichier
            de configuration L{filename}.
        @rtype: L{ConfFile}
        """
        filename = unicode(filename)
        instance = cls.by_filename(filename)
        if not instance:
            instance = cls(name=filename)
            DBSession.add(instance)
            DBSession.flush()
        return instance

    def __unicode__(self):
        """
        Représentation unicode de l'instance.

        @return: Nom du fichier de configuration.
        @rtype: C{unicode}
        """
        return self.name
