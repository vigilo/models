# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table PerfDataSource"""
from sqlalchemy import Column
from sqlalchemy.orm import relation
from sqlalchemy.types import Integer, Unicode, Float

from vigilo.models.session import DeclarativeBase, ForeignKey, DBSession
from vigilo.models.tables.secondary_tables import GRAPH_PERFDATASOURCE_TABLE
from vigilo.models.tables.host import Host

__all__ = ('PerfDataSource', )

class PerfDataSource(DeclarativeBase, object):
    """
    Informations sur une source de donnée d'un service.

    @ivar idperfdatasource: Identifiant auto-généré de la source de données.
    @ivar idhost: Identifiant de l'hôte auquel l'indicateur est rattaché.
    @ivar host: Instance de l'hôte auquel l'indicateur est rattaché.
    @ivar name: Nom de la source de données sur le disque dur.
    @ivar type: Type de la source de données
        (COUNTER, DERIVE, ABSOLUTE, GAUGE).
    @ivar label: Label affiché sur le graphique généré.
        (ex : name=ineth0 -> label=Données en entrée sur la carte réseau eth0)
    @ivar factor: Facteur de multiplication pour les valeurs en ordonnées.
        (ex : factor=8 pour conversion octets -> bits)
    @ivar max: Valeur maximale possible. Utilisée pour calculer un pourcentage
        d'utilisation de la ressource.
    """

    __tablename__ = 'perfdatasource'

    idperfdatasource = Column(
        Integer,
        primary_key=True, autoincrement=True,
    )

    idhost = Column(
        Integer,
        ForeignKey(
            Host.idhost,
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        nullable=False,
    )

    host = relation('Host', back_populates="perfdatasources",
                       lazy=True)

    name = Column(Unicode(255), nullable=False)

    # GAUGE, COUNTER, ...
    type = Column(Unicode(32), default=u'', nullable=False)

    label = Column(Unicode(255), default=u'')

    factor = Column(
        Float(precision=None, asdecimal=False),
        default=1.0, nullable=False)

    max = Column(Float(precision=None, asdecimal=False))

    graphs = relation('Graph', secondary=GRAPH_PERFDATASOURCE_TABLE,
                         back_populates='perfdatasources', lazy=True)

    def __init__(self, **kwargs):
        """Initialisation de la source de données de performance."""
        super(PerfDataSource, self).__init__(**kwargs)

    def __repr__(self):
        return "<%s \"%s\" on \"%s\">" % (self.__class__.__name__,
                                          str(self.name), str(self.host.name))

    @classmethod
    def by_host_and_source_name(cls, host, sourcename):
        """
        Renvoie une source de données concernant un service donné
        en fonction de son nom.

        @param cls: Classe à utiliser pour la récupération de la source.
        @type cls: C{type}
        @param host: Instance de L{Host} ou identifiant
            de l'hôte sur lequel porte la source de données.
        @type host: C{int} ou L{Host}
        @param sourcename: Nom de la source de données à récupérer.
        @type sourcename: C{unicode}
        @return: La source de données de performances dont le nom est
            C{sourcename} et qui porte sur le service C{service}.
        @rtype: L{PerfDataSource}
        """
        if isinstance(host, (int, long)):
            return DBSession.query(cls
                ).filter(cls.idhost == host
                ).filter(cls.name == sourcename
                ).first()

        return DBSession.query(cls
            ).filter(cls.idhost == host.idhost
            ).filter(cls.name == sourcename
            ).first()
