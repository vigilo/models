# -*- coding: utf-8 -*-
import transaction
from vigilo.models.vigilo_bdd_config import metadata
from vigilo.models.session import DBSession

metadata.bind = DBSession.bind

def drop():
    print "DROPping all tables"
    metadata.drop_all()
    transaction.commit()

def truncate():
    from vigilo.turbogears.websetup import populate_db

    for table in metadata.tables.items():
        print "Truncating table '%s'" % table[0]
        table[1].delete().execute()
        DBSession.flush()

    print "Re-inserting default data in tables"
    populate_db()
    transaction.commit()

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print "Please provide an action (either 'drop' or 'trunc')"
        sys.exit(1)

    action = sys.argv[1].lower()

    if action == 'drop':
        drop()
        sys.exit(0)

    if action == 'trunc' or action == 'truncate':
        truncate()
        sys.exit(0)

    print "Unknown action '%s'" % action
    sys.exit(2)

