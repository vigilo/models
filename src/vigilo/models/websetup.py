# -*- coding: utf-8 -*-
"""Peuple la base de données."""

import transaction
import pkg_resources

__all__ = [
    'populate_db',
    'init_db',
    'get_migration_scripts',
    'migrate_model',
]

def get_migration_scripts(module):
    """
    Renvoie un dictionnaire contenant la liste des scripts de migration
    disponibles, indexés par leur numéro de version.

    @param module: Nom du module à partir duquel les migrations seront
        chargées. Un sous-module "migration" doit exister sous ce module,
        contenant des scripts de migration pour le modèle. Les scripts
        doivent être nommés "<version>_<description>.py". Par exemple :
        "001_User_Email_Suppression_contrainte_not_null.py".
    @type  module: C{str}
    """
    files = pkg_resources.resource_listdir(module, 'migration')
    scripts = {}
    for f in files:
        if not f.endswith('.py') or f == '__init__.py':
            continue

        try:
            ver = int(f.split('_')[0], 10)
        except (ValueError, TypeError):
            continue

        scripts[ver] = f[:-3]
    return scripts

class MigrationActions(object):
    def __init__(self):
        self.deploy_force = False
        self.upgrade_vigireport = False

def migrate_model(bind, module, scripts, stop_at=None):
    """
    Met à jour le modèle à partir des scripts de migration fournis
    par le L{module}.

    @param bind: Connexion à la base de données.
    @type bind: C{Engine}
    @param module: Nom du module dont le modèle doit être migré.
    @type module: C{str}
    @param scripts: Dictionnaire contenant les noms des scripts de migration,
        indexés par leur numéro de version.
    @type scripts: C{dict}
    @param stop_at: Numéro du dernier script de migration à exécuter.
        Si omis, alors la migration s'effectue jusqu'au dernier script
        disponible, correspondant à la version la plus à jour.
    @type stop_at: C{int}
    @return: True si la migration a eu lieu (même lorsqu'au aucun changement
        n'a été effectué) ou False si le modèle en question n'existait pas.
    @rtype: C{bool}
    """
    from vigilo.models.session import DBSession
    from vigilo.models import tables

    if stop_at is None:
        stop_at = max(scripts.keys())

    module = unicode(module)

    print u"Searching for already installed version of '%s'" % module
    current_version = DBSession.query(tables.Version.version).filter(
                            tables.Version.name == module
                        ).scalar()


    if current_version:
        print u"Version %(version)d of %(module)s is already installed" % {
            'version': current_version,
            'module': module,
        }

        try:
            versions = scripts.keys()
            sorted(versions)
            actions = MigrationActions()
            for ver in versions:
                if ver <= current_version or ver > stop_at:
                    continue

                print u"Upgrading %(module)s to version %(version)d using " \
                    "the following changeset: '%(script)s'" % {
                    'module': module,
                    'version': ver,
                    'script': scripts[ver],
                }

                transaction.begin()

                try:
                    # On charge le script correspondant à la version en
                    # cours de traitement, à partir d'un dossier "migration"
                    # situé dans le répertoire du module donné en argument.
                    ep = pkg_resources.EntryPoint.parse(
                        'upgrade = %s.migration.%s:upgrade' % (
                            module,
                            scripts[ver],
                        )).load(require=False)

                    ep(bind, actions)
                    version = tables.Version()
                    version.name = module
                    version.version = ver
                    DBSession.merge(version)
                    DBSession.flush()
                except:
                    transaction.abort()
                    raise
                else:
                    transaction.commit()

            # La migration nécessite de redéployer le parc.
            if actions.deploy_force:
                print   "ATTENTION: Although the schema migration completed " \
                        "successfully,\n" \
                        "you should re-deploy your configuration using " \
                        "option --force to finish the migration."

            # La migration nécessite de mettre à jour VigiReport.
            if actions.upgrade_vigireport:
                print   "ATTENTION: The new schema is likely to be " \
                        "incompatible with that of your VigiReport " \
                        "installation.\n" \
                        "You should upgrade VigiReport as soon as possible."

            # Dans tous les cas, la migration nécessite de mettre à jour
            # les autres nœuds dans un modèle maître/esclaves.
            print   "If you have set up a master/backup replication cluster, " \
                    "you should also upgrade the model for other nodes " \
                    "in that cluster."

        except ImportError:
            # @TODO: log a warning/error or halt the process
            raise
        return True
    return False

def populate_db(bind, commit=True):
    """Placez les commandes pour peupler la base de données ici."""
    import logging
    LOGGER = logging.getLogger(__name__)

    from vigilo.models.session import DBSession, metadata

    # Chargement du modèle.
    from vigilo.models import tables

    # Création des tables
    print "Creating tables"
    metadata.create_all(bind=bind)

    module = 'vigilo.models'
    scripts = get_migration_scripts(module)
    max_version = max(scripts.keys())

    if not migrate_model(bind, module, scripts):
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
        version.name = unicode(module)
        version.version = max_version
        DBSession.add(version)
        DBSession.flush()

    # Spécifique projets
    from pkg_resources import working_set
    for entry in working_set.iter_entry_points("vigilo.models", "populate_db"):
        # Charge les tables spécifiques
        pop_db = entry.load()
        print "Setting up for %s" % entry.dist.project_name
        pop_db(bind)

    if commit:
        transaction.commit()
    print "Successfully setup"

def init_db(*args):
    """
    Cette fonction est appelée par le script vigilo-updatedb
    pour initialiser/mettre à jour la base de données de Vigilo.
    """
    from vigilo.common.conf import settings
    settings.load_module(__name__)

    from vigilo.models.configure import configure_db
    engine = configure_db(settings['database'], 'sqlalchemy_')
    populate_db(engine)
