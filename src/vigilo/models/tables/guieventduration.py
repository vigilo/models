# -*- coding: utf-8 -*-
# Copyright (C) 2006-2020 CS GROUP - France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Vue sur la durée des alarmes
"""

from sqlalchemy import Column
from sqlalchemy.types import Integer, Unicode

from vigilo.models.session import DeclarativeBase, DDL

from vigilo.models.tables.event import Event
from vigilo.models.tables.correvent import CorrEvent

class GuiEventDuration(DeclarativeBase, object):
    """
    Table factice correspondant à une vue dans la base de données.
    """
    __tablename__ = 'vigilo_guieventduration'

    idcorrevent = Column(
        Integer,
        nullable=False,
        primary_key=True,
    )

    duration = Column(
        Integer,
        nullable=False,
    )

# Permet d'indiquer qu'il s'agit d'une vue et non pas d'une table réelle.
GuiEventDuration.__table__.info = {'vigilo_view': True}


# Suppression de la table automatiquement générée par SQLAlchemy.
DDL(
    "DROP TABLE IF EXISTS %(fullname)s",
    'after-create',
    GuiEventDuration.__table__,
)


# Création de la vue pour PostgreSQL.
DDL(
    r"""
    CREATE OR REPLACE VIEW %(fullname)s AS
        SELECT %(correvent_table)s.idcorrevent,
        EXTRACT(EPOCH FROM (%(event_table)s."timestamp" - %(correvent_table)s.timestamp_active)) AS duration
        FROM %(correvent_table)s
        JOIN %(event_table)s
            ON %(event_table)s.idevent = %(correvent_table)s.idcause
    """,
    'after-create',
    GuiEventDuration.__table__,
    dialect=('postgres', 'postgresql'),
    context={
        'correvent_table': CorrEvent.__tablename__,
        'event_table': Event.__tablename__,
    },
)


# Création de la vue pour SQLite.
DDL(
    r"""
    CREATE VIEW IF NOT EXISTS %(fullname)s AS
        SELECT %(correvent_table)s.idcorrevent,
        (CAST(strftime('%%s', %(event_table)s."timestamp") AS INTEGER) -
         CAST(strftime('%%s', %(correvent_table)s.timestamp_active) AS INTEGER)) AS duration
        FROM %(correvent_table)s
        JOIN %(event_table)s
            ON %(event_table)s.idevent = %(correvent_table)s.idcause
    """,
    'after-create',
    GuiEventDuration.__table__,
    dialect='sqlite',
    context={
        'correvent_table': CorrEvent.__tablename__,
        'event_table': Event.__tablename__,
    },
)


# CREATE/DROP VIEW IF (NOT) EXISTS a été ajouté dans SQLite 3.3.8.
# Pour plus d'information : http://www.sqlite.org/changes.html
# On suppose que SQLite 3.5.4 ou plus est disponible.
DDL(
    "DROP VIEW IF EXISTS %(fullname)s",
    'before-drop',
    GuiEventDuration.__table__,
)

DDL(
    "CREATE TABLE %(fullname)s (foo INTEGER)",
    'before-drop',
    GuiEventDuration.__table__,
)
