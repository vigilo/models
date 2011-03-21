# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Permissions"""
from sqlalchemy import Column
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.orm import relation
from sqlalchemy.schema import UniqueConstraint

from vigilo.models.session import DeclarativeBase, ForeignKey
from vigilo.models.tables.usergroup import UserGroup
from vigilo.models.tables.group import Group

__all__ = ('DataPermission', )

class DataPermission(DeclarativeBase, object):
    """
    Cette classe définit une permission sur des données.
    """

    __tablename__ = 'datapermission'
    __table_args__ = (
        UniqueConstraint('idusergroup', 'idgroup'),
        {}
    )

    idusergroup = Column(
        Integer,
        ForeignKey(
            UserGroup.idgroup,
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        autoincrement=False, primary_key=True,
    )

    usergroup = relation('UserGroup', back_populates='datapermissions')

    idgroup = Column(
        Integer,
        ForeignKey(
            Group.idgroup,
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        autoincrement=False, primary_key=True,
    )

    group = relation('Group', back_populates='datapermissions')

    access = Column(
        Unicode(1),
        nullable=False,
    )

    def __init__(self, **kwargs):
        """Initialisation des informations concernant la permission."""
        super(DataPermission, self).__init__(**kwargs)

    def __unicode__(self):
        return "<%s - %s>" % (unicode(self.group), unicode(self.usergroup))
