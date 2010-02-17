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
    DBSession.flush()

    group = models.UserGroup()
    group.group_name = u'managers'
    group.users.append(manager)
    DBSession.add(group)
    DBSession.flush()

    permission = models.Permission()
    permission.permission_name = u'manage'
    permission.usergroups.append(group)
    DBSession.add(permission)
    DBSession.flush()

    editor = models.User()
    editor.user_name = u'editor'
    editor.email = u'editor@somedomain.com'
    editor.fullname = u'Editor'
    editor.password = u'editpass'
    DBSession.add(editor)
    DBSession.flush()

    group = models.UserGroup()
    group.group_name = u'editors'
    group.users.append(editor)
    DBSession.add(group)
    DBSession.flush()

    permission = models.Permission()
    permission.permission_name = u'edit'
    permission.usergroups.append(group)
    DBSession.add(permission)
    DBSession.flush()

    version = models.Version()
    version.name = u'vigilo.models'
    version.version = models.VIGILO_MODEL_VERSION
    DBSession.add(version)
    DBSession.flush()

    DBSession.add(models.StateName(statename=u'OK', order=0))
    DBSession.add(models.StateName(statename=u'UNKNOWN', order=1))
    DBSession.add(models.StateName(statename=u'WARNING', order=2))
    DBSession.add(models.StateName(statename=u'CRITICAL', order=3))
    DBSession.add(models.StateName(statename=u'UP', order=0))
    DBSession.add(models.StateName(statename=u'UNREACHABLE', order=1))
    DBSession.add(models.StateName(statename=u'DOWN', order=3))
    DBSession.flush()

    transaction.commit()
    print "Successfully setup"

def init_db():
    """
    Cette fonction est appelée par le script vigiboard-init-db
    pour initialiser la base de données de Vigiboard.
    """
    from vigilo.common.conf import settings
    settings.load_module(__name__)

    from vigilo.models.configure import configure_db
    engine = configure_db(settings['database'], 'sqlalchemy_')
    populate_db(engine)

