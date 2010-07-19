# -*- coding: utf-8 -*-

"""
Module permettant de créer facilement des générateur de données factices pour
les démonstrations.
"""

from pkg_resources import resource_listdir, working_set

__all__ = ("samples")

samples = {}

def list_samples(module):
    mod_samples = {}
    for subfile in resource_listdir(module, ""):
        if not subfile.endswith(".py"):
            continue
        submodule = subfile[:-3]
        if submodule in ["__init__", "functions"]:
            continue
        mod_samples[submodule] = "%s.%s" % (module, submodule)
    return mod_samples

samples.update(list_samples("vigilo.models.demo"))

# Spécifique projets
for entry in working_set.iter_entry_points("vigilo.models.demo", "samples"):
    samples.update(list_samples(entry.module_name))



def run_demo():
    import optparse
    from vigilo.common.gettext import translate_narrow
    _ = translate_narrow(__name__)

    parser = optparse.OptionParser("Usage: %prog sample1 [sample2...]")
    opts, args = parser.parse_args()
    if not args:
        parser.error(_("No sample selected. Available samples: %s")
                % ", ".join(samples.keys()))
        return

    from vigilo.common.conf import settings
    settings.load_module('vigilo.models')

    from vigilo.models.configure import configure_db
    configure_db(settings['database'], 'sqlalchemy_',
        settings['database']['db_basename'])

    import atexit
    def commit_on_exit():
        """
        Effectue un COMMIT sur la transaction à la fin de l'exécution
        du script d'insertion des données de test.
        """
        import transaction, sqlalchemy
        try:
            transaction.commit()
        except sqlalchemy.exc.InvalidRequestError:
            transaction.abort()
    atexit.register(commit_on_exit)

    for sample in args:
        if sample not in samples:
            parser.error(_("Sample '%s' cannot be found.") % sample)
            return
        module = __import__(samples[sample], globals(), locals(), ["main"], -1)
        module.main()


