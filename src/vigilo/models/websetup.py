# -*- coding: utf-8 -*-
"""Peuple la base de données."""

import logging

import transaction

__all__ = ['populate_db', 'init_db']

LOGGER = logging.getLogger(__name__)


def populate_db(bind):
    """Placez les commandes pour peupler la base de données ici."""
    from vigilo.models.configure import DBSession, metadata

    # Chargement du modèle.
    from vigilo import models

    # Création des tables
    print "Creating tables"
    metadata.create_all(bind=bind)

    # Création d'un jeu de données par défaut.
    manager = models.User()
    manager.user_name = u'manager'
    manager.email = u'manager@somedomain.com'
    manager.fullname = u'Manager'
    manager.password = u'managepass'
    DBSession.add(manager)

    group = models.UserGroup()
    group.group_name = u'managers'
    group.users.append(manager)
    DBSession.add(group)

    permission = models.Permission()
    permission.permission_name = u'manage'
    permission.usergroups.append(group)
    DBSession.add(permission)

    editor = models.User()
    editor.user_name = u'editor'
    editor.email = u'editor@somedomain.com'
    editor.fullname = u'Editor'
    editor.password = u'editpass'
    DBSession.add(editor)

    group = models.UserGroup()
    group.group_name = u'editors'
    group.users.append(editor)
    DBSession.add(group)

    permission = models.Permission()
    permission.permission_name = u'edit'
    permission.usergroups.append(group)
    DBSession.add(permission)

    version = models.Version()
    version.name = u'vigilo.models'
    version.version = models.VIGILO_MODEL_VERSION
    DBSession.add(version)

    DBSession.flush()
    transaction.commit()
    print "Successfully setup"

def init_db():
    """
    Cette fonction est appelée par le script vigiboard-init-db
    pour initialiser la base de données de Vigiboard.
    """
    from ConfigParser import SafeConfigParser
    from optparse import OptionParser
    from vigilo.models.configure import configure_db

    parser = OptionParser()
    parser.add_option('-c', '--config', dest='config_file',
        default='/etc/vigilo/models/settings.ini',
        help='Path to the INI configuration file to use.', metavar='FILE')

    options = parser.parse_args()[0]

    ini_parser = SafeConfigParser()
    ini_parser.read(options.config_file)

    settings = dict(ini_parser.items('vigilo.models'))
    engine = configure_db(settings, 'sqlalchemy.')
    populate_db(engine)

