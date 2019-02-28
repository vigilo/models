# -*- coding: utf-8 -*-
# Copyright (C) 2006-2019 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Vue des événements en heure UTC
"""

from sqlalchemy import Column
from sqlalchemy.types import Integer, DateTime, Text

from vigilo.models.session import DeclarativeBase, DDL

from vigilo.models.tables.event import Event

class GuiEvent(DeclarativeBase, object):
    """
    Table factice correspondant à une vue dans la base de données.
    """
    __tablename__ = 'vigilo_guievent'

    idevent = Column(
        Integer,
        nullable=False,
        primary_key=True,
    )

    timestamp = Column(
        DateTime(timezone=True),
        nullable=False,
    )

    idsupitem = Column(
        Integer,
        nullable=False,
    )

    current_state = Column(
        Integer,
        nullable=False,
    )

    initial_state = Column(
        Integer,
        nullable=False,
    )

    peak_state = Column(
        Integer,
        nullable=False,
    )

    message = Column(
        Text(length=None, convert_unicode=True),
        nullable=False,
    )

# Permet d'indiquer qu'il s'agit d'une vue et non pas d'une table réelle.
GuiEvent.__table__.info = {'vigilo_view': True}


# Suppression de la table automatiquement générée par SQLAlchemy.
DDL(
    "DROP TABLE IF EXISTS %(fullname)s",
    'after-create',
    GuiEvent.__table__,
)


# Création de la vue pour PostgreSQL.
DDL(
    r"""
    CREATE OR REPLACE VIEW %(fullname)s AS
        SELECT %(event_table)s.idevent,
            timezone('UTC'::text, ((%(event_table)s."timestamp" || ' '::text) || conf.setting)::TIMESTAMP WITH TIME ZONE) AS "timestamp",
            %(event_table)s.idsupitem,
            %(event_table)s.current_state,
            %(event_table)s.initial_state,
            %(event_table)s.peak_state,
            %(event_table)s.message
        FROM %(event_table)s
        JOIN pg_settings conf
            ON conf.name = 'TimeZone'::text;
    """,
    'after-create',
    GuiEvent.__table__,
    dialect=('postgres', 'postgresql'),
    context={
        'event_table': Event.__tablename__,
    },
)


# Création de la vue pour SQLite.
DDL(
    r"""
    CREATE VIEW IF NOT EXISTS %(fullname)s AS
        SELECT vigilo_event.idevent,
            datetime(%(event_table)s."timestamp", 'utc') AS "timestamp",
            %(event_table)s.idsupitem,
            %(event_table)s.current_state,
            %(event_table)s.initial_state,
            %(event_table)s.peak_state,
            %(event_table)s.message
        FROM %(event_table)s;
    """,
    'after-create',
    GuiEvent.__table__,
    dialect='sqlite',
    context={
        'event_table': Event.__tablename__,
    },
)


# CREATE/DROP VIEW IF (NOT) EXISTS a été ajouté dans SQLite 3.3.8.
# Pour plus d'information : http://www.sqlite.org/changes.html
# On suppose que SQLite 3.5.4 ou plus est disponible.
DDL(
    "DROP VIEW IF EXISTS %(fullname)s",
    'before-drop',
    GuiEvent.__table__,
)

DDL(
    "CREATE TABLE %(fullname)s (foo INTEGER)",
    'before-drop',
    GuiEvent.__table__,
)
