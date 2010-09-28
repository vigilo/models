# -*- coding: utf-8 -*-
"""Peuple la base de données."""

import transaction
import pkg_resources

__all__ = [
    'populate_db',
    'init_db',
    'VIGILO_MODELS_VERSION',
]

# Numéro de version du modèle, il sera incrémenté pour chaque nouvelle
# version livrée au client. Il sera utilisé par les scripts de mise à jour
# de Vigilo afin d'importer les données d'une ancienne version du modèle
# vers la nouvelle version (permet d'assurer la rétro-compatibilité).
VIGILO_MODELS_VERSION = 5

def populate_db(bind):
    """Placez les commandes pour peupler la base de données ici."""
    import logging
    LOGGER = logging.getLogger(__name__)

    from vigilo.models.session import DBSession, metadata

    # Chargement du modèle.
    from vigilo.models import tables

    # Création des tables
    print "Creating tables"
    metadata.create_all(bind=bind)

    # Création d'un jeu de données par défaut.
    print "Checking for an already existing model"
    current_version = DBSession.query(tables.Version.version).filter(
                            tables.Version.name == u'vigilo.models'
                        ).scalar()

    if current_version:
        print "Version %d of the model is already installed" % current_version
        files = pkg_resources.resource_listdir('vigilo.models.migration', '')
        scripts = []
        for f in files:
            if not f.endswith('.py') or f == '__init__.py':
                continue
            scripts.append(f[:-3])
        scripts.sort()

        try:
            for script in scripts:
                try:
                    ver = int(script.split('_')[0])
                except ValueError:
                    continue

                if ver <= current_version or ver > VIGILO_MODELS_VERSION:
                    continue

                print "Upgrading to version %(version)d using the " \
                    "following changeset: '%(script)s'" % {
                    'version': ver,
                    'script': script,
                }

                transaction.begin()

                try:
                    ep = pkg_resources.EntryPoint.parse(
                        'upgrade = vigilo.models.migration.%s:upgrade' % script
                        ).load(require=False)
                    # @FIXME: le 2ème argument est le nom du cluster.
                    # Il ne devrait probablement pas être hard-codé...
                    ep(bind, 'vigilo')
                    version = tables.Version()
                    version.name = u'vigilo.models'
                    version.version = ver
                    DBSession.merge(version)
                    DBSession.flush()
                except:
                    transaction.abort()
                    raise
                else:
                    transaction.commit()
        except ImportError:
            # @TODO: log a warning/error or halt the process
            raise

    else:
        print "Setting up the generic tables"
        manager = tables.User()
        manager.user_name = u'manager'
        manager.email = u'manager@somedomain.com'
        manager.fullname = u'Manager'
        manager.password = u'managepass'
        DBSession.add(manager)
        DBSession.flush()

        group = tables.UserGroup()
        group.group_name = u'managers'
        group.users.append(manager)
        DBSession.add(group)
        DBSession.flush()

        DBSession.add(tables.StateName(statename=u'OK', order=0))
        DBSession.add(tables.StateName(statename=u'UNKNOWN', order=1))
        DBSession.add(tables.StateName(statename=u'WARNING', order=2))
        DBSession.add(tables.StateName(statename=u'CRITICAL', order=3))
        DBSession.add(tables.StateName(statename=u'UP', order=0))
        DBSession.add(tables.StateName(statename=u'UNREACHABLE', order=1))
        DBSession.add(tables.StateName(statename=u'DOWN', order=3))
        DBSession.flush()

        version = tables.Version()
        version.name = u'vigilo.models'
        version.version = VIGILO_MODELS_VERSION
        DBSession.add(version)
        DBSession.flush()

    # Spécifique projets
    from pkg_resources import working_set
    for entry in working_set.iter_entry_points("vigilo.models", "populate_db"):
        # Charge les tables spécifiques
        pop_db = entry.load()
        print "Setting up for %s" % entry.dist.project_name
        pop_db(bind)

    transaction.commit()
    print "Successfully setup"

def init_db(*args):
    """
    Cette fonction est appelée par le script vigiboard-init-db
    pour initialiser la base de données de Vigiboard.
    """
    from vigilo.common.conf import settings
    settings.load_module(__name__)

    from vigilo.models.configure import configure_db
    engine = configure_db(settings['database'], 'sqlalchemy_',
        settings['database']['db_basename'])
    populate_db(engine)
