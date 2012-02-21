# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>
"""
Script permettant de modifier le mot de passe
d'un utilisateur dans la base de données de Vigilo.
"""

import os, pwd, sys
import argparse
import pkg_resources

from vigilo.common.argparse import prepare_argparse
from vigilo.common.gettext import translate, translate_narrow
_ = translate(__name__)
N_ = translate_narrow(__name__)

__all__ = (
    'main',
)

def _parse_args(args):
    """
    Analyse les paramètres passés à ce script et en déduit
    les options actives.

    @param args: Paramètres passés au script via la ligne de commandes.
    @type args: C{list}
    @return: Un tuple avec les (options, arguments) obtenus après analyse.
    @rtype: C{tuple}
    """
    # Options générales.
    common_options = argparse.ArgumentParser()
    common_options.add_argument("-c", "--config", type=str,
        help=N_("Load configuration from this file."))

    # Parser de plus haut niveau.
    parser = argparse.ArgumentParser(
        add_help=False,
        parents=[common_options],
    )
    subparsers = parser.add_subparsers(dest='action', title=N_('Commands'))

    dist = pkg_resources.get_distribution('vigilo-models')
    # Pylint croit que "dist" est de type <str> ...
    #pylint: disable-msg=E1103
    parser.add_argument("-V", "--version", action="version",
        version="%%(prog)s %s" % dist.version,
        help=N_("Display this program's version and exit."))

    # Commande d'ajout/mise à jour de permissions.
    parser_add = subparsers.add_parser(
        "add",
        add_help=False,
        parents=[common_options],
        help=N_("Add or update permissions for the given usergroup "
                "to a certain group of objects."),
    )
    parser_add.set_defaults(commit=True) # appeler transaction.commit().
    parser_add.add_argument("usergroup", type=str,
        help=N_("Usergroup to act upon."))
    parser_add.add_argument(
        "object_type",
        choices=["monitored", "map", "graph"],
        help=N_("Type of object group to act upon: "
                "'monitored' for groups of monitored items, "
                "'map' for groups of maps, "
                "or 'graph' for groups of graphs"))
    parser_add.add_argument("object_group", type=str,
        help=N_("Group to act upon. This can be either the full path "
                "to the group, or a relative one."))
    parser_add.add_argument("permission",
        choices=["ro", "rw"],
        help=N_("Type of permission to give: 'ro' (%(ro)s) "
                "or 'rw' (%(rw)s).") % {
                    'ro': N_('read-only'),
                    'rw': N_('read/write'),
                })
    parser_add.add_argument("-b", "--batch", action="store_true",
        help=N_("In case multiple groups of objects are found "
                "with the given name and type, apply the permissions "
                "for all of them at once."))
    parser_add.add_argument("-u", "--update", action="store_true",
        help=N_("Resolve conflicts by updating existing permissions."))

    # Commande de suppression de permissions.
    #
    # L'interface est similaire à celle de la commande "add", sauf qu'il
    # n'est pas nécessaire de spécifier la permission (ro/rw)
    # à supprimer : un groupe d'utilisateur ne peut avoir qu'un seul type
    # de permission sur un groupe d'objets à la fois.
    parser_remove = subparsers.add_parser(
        "remove",
        add_help=False,
        parents=[common_options],
        help=N_("Remove permissions for a given usergroup on a certain "
                "group of objects."),
    )
    parser_remove.set_defaults(commit=True) # appeler transaction.commit().
    parser_remove.add_argument("usergroup", type=str,
        help=N_("Usergroup to act upon."))
    parser_remove.add_argument(
        "object_type",
        choices=["monitored", "map", "graph"],
        help=N_("Type of object group to act upon: "
                "'monitored' for groups of monitored items, "
                "'map' for groups of maps, "
                "or 'graph' for groups of graphs."))
    parser_remove.add_argument("object_group", type=str,
        help=N_("Group to act upon. This can be either the full path "
                "to the group, or a relative one."))
    parser_remove.add_argument("permission",
        choices=["ro", "rw"], default=None, nargs="?",
        help=N_("Type of permission to give: 'ro' (%(ro)s) "
                "or 'rw' (%(rw)s).") % {
                    'ro': N_('read-only'),
                    'rw': N_('read/write'),
                })
    parser_remove.add_argument("-b", "--batch", action="store_true",
        help=N_("In case multiple groups of objects are found "
                "with the given name and type, apply the permissions "
                "for all of them at once."))

    # Commande pour lister les différents groupes
    # pour un type d'objets donné.
    parser_list = subparsers.add_parser(
        "list",
        add_help=False,
        parents=[common_options],
        help=N_("Display the list of existing usergroups and other "
                "groups of objects."),
    )
    parser_list.add_argument(
        "object_type",
        choices=["monitored", "map", "graph", "user"],
        help=N_("Type of object group to act upon: "
                "'monitored' for groups of monitored items, "
                "'map' for groups of maps, "
                "'graph' for groups of graphs, "
                "or 'user' for usergroups."))

    # Alias pour "add --update ...".
    subparsers.add_parser("update",
        add_help=False, parents=[parser_add],
        help=N_("Alias for '%(prog)s add --update'.")
    ).set_defaults(action="add", update=True)
    # Aliases pour la commande "remove".
    subparsers.add_parser("delete",
        add_help=False, parents=[parser_remove],
        help=N_("Alias for '%(prog)s remove'."),
    ).set_defaults(action="remove")
    subparsers.add_parser("rm",
        add_help=False, parents=[parser_remove],
        help=N_("Alias for '%(prog)s remove'."),
    ).set_defaults(action="remove")
    subparsers.add_parser("del",
        add_help=False, parents=[parser_remove],
        help=N_("Alias for '%(prog)s remove'."),
    ).set_defaults(action="remove")

    return parser.parse_args(args)


def _prepare_db(options):
    """
    Configure l'accès à la base de données Vigilo.

    @param options: Options et arguments passés au script
        sur la ligne de commandes.
    @type options: C{argparse.Namespace}
    @return: Un booléen qui indique si la configuration
        de la base de données s'est bien déroulée ou non.
    @rtype: C{bool}
    """
    from vigilo.common.conf import settings
    if options.config:
        settings.load_file(options.config)
    else:
        settings.load_module(__name__)

    from vigilo.models.configure import configure_db
    try:
        configure_db(settings['database'], 'sqlalchemy_')
    except KeyError:
        print _('No database configuration found')
        return False
    return True


def main(*args):
    """
    Point d'entrée pour le script de réglage des permissions.
    """
    prepare_argparse()
    options = _parse_args(sys.argv[1:])

    # Map les aliases vers la commande "standard".
    aliases = {
        'delete': 'remove',
        'rm': 'remove',
        'del': 'remove',
        'update': 'add',
    }

    current_user = pwd.getpwuid(os.getuid())
    username = current_user.pw_name
    # Seul "root" (UID 0) est autorisé à changer les permissions
    # dans Vigilo de façon arbitraire.
    if current_user.pw_uid != 0:
        print _("You must be root to use this script.")
        sys.exit(1)

    if not _prepare_db(options):
        # Inutile d'afficher un message d'erreur ici :
        # _prepare_db() le fait déjà.
        sys.exit(1)

    from vigilo.models.scripts.permissions import commands
    # On récupère la commande à exécuter (en gérant le cas des aliases)
    # et on appelle la fonction associée.
    cmd = aliases.get(options.action, options.action)
    func = getattr(commands, "cmd_" + cmd)
    sys.exit(func(options))
