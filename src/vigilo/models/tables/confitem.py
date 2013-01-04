# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2013 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèle pour la table confitem"""
from sqlalchemy import Column
from sqlalchemy.types import Unicode, Integer
from sqlalchemy.orm import relation
from sqlalchemy.schema import Index

from vigilo.models.session import DeclarativeBase, DBSession, \
                                    ForeignKey, PrefixedTables
from vigilo.models.tables import SupItem, Host, LowLevelService

class ConfItemIndexMeta(PrefixedTables):
    """
    Cette méta-classe ajoute un index sur les colonnes "name"
    et "idsupitem", utilisée par VigiConf lors de la mise à jour
    des entrées de la table L{ConfItem}.
    """
    def __init__(mcs, *args, **kw):
        if getattr(mcs, '_decl_class_registry', None) is None:
            return

        super(ConfItemIndexMeta, mcs).__init__(*args, **kw)
        Index(
            'ix_%s_key' % mcs.__tablename__,
            mcs.name, mcs.idsupitem,
            unique=True
        )

class ConfItemMixin(object):
    """
    Ce mixin permet simplement d'intégrer la méta-classe,
    afin d'éviter un conflit entre méta-classes dans ConfItem.
    """
    __metaclass__ = ConfItemIndexMeta

class ConfItem(DeclarativeBase, ConfItemMixin):
    """
    Un confitem (élément de configuration) est associé à un élément
    supervisé.

    Typiquement utilisé pour associer une directive nagios
    à un hote ou un service de bas niveau.

    @ivar name: Nom du confitem.
    @ivar value: Valeur associée au confitem.
    @ivar supitem: élément supervisé (C{SupItem}) auxquel
        le confitem est rattaché.
    """

    __tablename__ = 'confitem'

    idconfitem = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name = Column(Unicode(50), nullable=False)

    value = Column(Unicode(100), nullable=False)

    idsupitem = Column(
        Integer,
        ForeignKey(
            SupItem.idsupitem,
            onupdate='CASCADE',
            ondelete='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        nullable=False,
    )

    supitem = relation('SupItem')

    def __init__(self, **kwargs):
        """Initialise un confitem."""
        super(ConfItem, self).__init__(**kwargs)

    @classmethod
    def by_host_confitem_name(cls, hostname, name):
        """
        Renvoie le ConfItem dont le nom d'hôte
        est L{hostname} et le nom est L{name}.

        @param hostname: Nom de l'hôte auquel est rattaché le confitem.
        @type hostname: C{unicode}
        @param name: Nom du confitem voulu.
        @type name: C{unicode}
        @return: Le ConfItem demandé.
        @rtype: L{ConfItem} ou None
        """
        return DBSession.query(cls).join(
                (Host, Host.idsupitem == cls.idsupitem)
            ).filter(Host.name == unicode(hostname)
            ).filter(cls.name == unicode(name)
            ).first()

    @classmethod
    def by_host_service_confitem_name(cls, hostname, servicename, name):
        """
        Renvoie le ConfItem dont le nom d'hôte
        est L{hostname} et le nom est L{name}.

        @param hostname: Nom de l'hôte auquel est rattaché le service.
        @type hostname: C{unicode}
        @param servicename: Nom du service voulu.
        @type servicename: C{unicode}
        @param name: Nom du confitem voulu.
        @type name: C{unicode}
        @return: Le ConfItem demandé.
        @rtype: L{ConfItem} ou None
        """
        return DBSession.query(cls).join(
                (LowLevelService, LowLevelService.idsupitem == cls.idsupitem)
            ).join(
                (Host, Host.idsupitem == LowLevelService.idhost)
            ).filter(Host.name == unicode(hostname)
            ).filter(LowLevelService.servicename == unicode(servicename)
            ).filter(cls.name == unicode(name)
            ).first()


    def __unicode__(self):
        """
        Représentation unicode du confitem.

        @return: Le nom du confitem.
        @rtype: C{unicode}
        """
        return self.name
