# vim: set fileencoding=utf-8 sw=4 ts=4 et :

"""
A session class.
Turbogears components have their own in the vigiboard package
and shouldn't use this.

Thread-local, autoflush, no autocommit.
"""

from sqlalchemy.engine import engine_from_config
from sqlalchemy.orm import scoped_session, sessionmaker
from vigilo.common.conf import settings

__all__ = ( 'DBSession', )

DBSession = scoped_session(sessionmaker(autoflush=True, autocommit=False))

engine = engine_from_config(settings['VIGILO_SQLALCHEMY'], prefix='')

