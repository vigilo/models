# vim: set fileencoding=utf-8 sw=4 ts=4 et :

"""
A session class.
Turbogears components have their own in the vigiboard package
and shouldn't use this.

Thread-local, autoflush, no autocommit.
"""
# Import pour l'initialisation issue de Turbogears
from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy import create_engine

# import la version non valide
# from sqlalchemy.engine import engine_from_config

from sqlalchemy.orm import scoped_session, sessionmaker
from vigilo.common.conf import settings

__all__ = ( 'DBSession', )

# Ne fonctionne pas
#DBSession = scoped_session(sessionmaker(autoflush=True, autocommit=False))
#DBSession.bind = engine_from_config(settings['VIGILO_SQLALCHEMY'], prefix='')

# Initialisation issue de Turbogears
maker = sessionmaker(autoflush=True, autocommit=False,
                                     extension=ZopeTransactionExtension())
DBSession = scoped_session(maker)
engine = create_engine(settings['VIGILO_SQLALCHEMY']['url'], echo=True)
DBSession.configure(bind=engine)

