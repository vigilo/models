# -*- coding: utf-8 -*-
import transaction
from vigilo.models.configure import DBSession, metadata, configure_db
from vigilo.models.websetup import populate_db
import sqlalchemy

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

    config_db()
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

