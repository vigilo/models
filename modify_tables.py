# -*- coding: utf-8 -*-
# Copyright (C) 2006-2015 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

import transaction
import sqlalchemy

from vigilo.common.conf import settings
settings.load_module('vigilo.models')

from vigilo.models.configure import configure_db
configure_db(settings['database'], 'sqlalchemy_')

from vigilo.models.session import DBSession, metadata
from vigilo.models.websetup import populate_db
from vigilo.models import tables

def drop():
    print "DROPping all tables"
    metadata.drop_all()
    transaction.commit()

def truncate():
    for table in metadata.tables.items():
        print "Truncating table '%s'" % table[0]
        try:
            table[1].delete().execute()
        except sqlalchemy.exc.ProgrammingError:
            print "Table %s does not exist" % table[0]
        DBSession.flush()

    print "Re-inserting default data in tables"
    populate_db(None)
    transaction.commit()

def create():
    populate_db(None)
    transaction.commit()

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print "Usage: python %s <create/drop/trunc>" % sys.argv[0]
        sys.exit(1)

    action = sys.argv[1].lower()

    if action == 'create':
        create()
        sys.exit(0)

    if action == 'drop':
        drop()
        sys.exit(0)

    if action == 'trunc' or action == 'truncate':
        truncate()
        sys.exit(0)

    print "Unknown action '%s'" % action
    sys.exit(2)
