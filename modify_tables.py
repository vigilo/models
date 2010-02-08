# -*- coding: utf-8 -*-
import transaction
from vigilo.models.configure import DBSession, metadata, configure_db

def config_db():
    from ConfigParser import SafeConfigParser

    parser = SafeConfigParser()
    parser.read('settings.ini')
    settings = dict(parser.items('vigilo.models'))
    configure_db(settings, 'sqlalchemy.')

def drop():
    print "DROPping all tables"
    metadata.drop_all()
    transaction.commit()

def truncate():
    from vigilo.models.websetup import populate_db

    for table in metadata.tables.items():
        print "Truncating table '%s'" % table[0]
        table[1].delete().execute()
        DBSession.flush()

    print "Re-inserting default data in tables"
    populate_db(None)
    transaction.commit()

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print "Usage: python %s <drop/trunc>" % sys.argv[0]
        sys.exit(1)

    config_db()
    action = sys.argv[1].lower()

    if action == 'drop':
        drop()
        sys.exit(0)

    if action == 'trunc' or action == 'truncate':
        truncate()
        sys.exit(0)

    print "Unknown action '%s'" % action
    sys.exit(2)

