# -*- coding: utf-8 -*-
# Copyright (C) 2006-2020 CS GROUP - France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Module permettant de créer facilement des générateurs de données factices
pour les démonstrations.
"""

from pkg_resources import resource_listdir, working_set

__all__ = ("samples", )

samples = {}

def list_samples(module):
    """
    Renvoie la liste des scénarios de démonstration
    fournis par un module donné.

    @param module: Module à interroger.
    @type module: C{str}
    @return: Dictionnaire contenant l'emplacement des différents
        scénarios de démonstration fournis par le module,
        indexés par leur nom.
    @rtype: C{dict}
    """
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
    """
    Insère des données d'exemple dans la base de données
    à partir d'un scénario de démonstration.
    Plusieurs scénarios différents peuvent être cumulés
    en passant leurs différents noms à ce programme.
    """
    import optparse
    from vigilo.common.gettext import translate_narrow
    _ = translate_narrow(__name__)

    parser = optparse.OptionParser("Usage: %prog sample1 [sample2...]")
    args = parser.parse_args()[1]
    if not args:
        parser.error(_("No sample selected. Available samples: %s")
                % ", ".join(samples.keys()))
        return

    from vigilo.common.conf import settings
    settings.load_module('vigilo.models')

    from vigilo.models.configure import configure_db
    configure_db(settings['database'], 'sqlalchemy_')

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
