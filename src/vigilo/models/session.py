# vim: set fileencoding=utf-8 sw=4 ts=4 et :

"""
A session class.

Update: two, due to the zodb's leaky abstraction.

Thread-local, autoflush, no autocommit.

Turbogears components have their own in the vigiboard package
and shouldn't use this.

We have a dilemma when writing model methods: should those use the raw session,
always available but less featureful and bypassing zope transactions,
or the ZTE transaction?

I'll go with the ZTE one. Because otherwise we might be bypassing
the ZTE session context. Also models shouldn't need to commit.

Because of that I'm forced to use the ZTE variant everywhere,
and to use the zope way to commit transactions.

Or I could move the DBSession-using models to a different package,
to ensure that there is no dependency that pulls them.
"""

from sqlalchemy.engine import engine_from_config
from sqlalchemy.orm import scoped_session, sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension

from vigilo.common.conf import settings

__all__ = ( 'DBSession', )

"""
Raw session.

We can commit on it and stuff.
"""
RawDBSession = scoped_session(sessionmaker(autoflush=True, autocommit=False))
RawDBSession.bind = engine_from_config(settings['VIGILO_SQLALCHEMY'], prefix='')

"""
ZTE session.

We must go through transaction (a zodb extraction) to commit, rollback.
There's also a session context to hold managed data, and the
ZopeTransactionExtension makes that mostly transparent.
The ZopeTransactionExtension prevents us
from committing, etc, the session directly.
"""
ZTEDBSession = scoped_session(sessionmaker(autoflush=True, autocommit=False,
    extension=ZopeTransactionExtension()))
ZTEDBSession.bind = engine_from_config(settings['VIGILO_SQLALCHEMY'], prefix='')

DBSession = ZTEDBSession

