# vim: set fileencoding=utf-8 sw=4 ts=4 et :

"""
A session class.
Turbogears components have their own in the vigiboard package
and shouldn't use this.

Thread-local, autoflush, no autocommit.
"""

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from vigilo.common.conf import settings

__all__ = ( 'DBSession', )

DBSession = scoped_session(sessionmaker(autoflush=True, autocommit=False))

engine = create_engine(settings['VIGILO_MODELS'])

DBSession.configure(bind=engine)

