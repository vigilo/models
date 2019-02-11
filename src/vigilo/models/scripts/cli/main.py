# -*- coding: utf-8 -*-
# Copyright (C) 2018-2019 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>
"""
Script permettant d'effectuer diverses opérations de gestion dans Vigilo,
liées aux utilisateurs, aux groupes d'utilisateurs et aux permissions.
"""

from __future__ import print_function
import os, pwd, sys
import warnings

from pkg_resources import working_set, get_distribution
import argparse
import transaction

from vigilo.common.logging import get_logger
from vigilo.common.argparse import prepare_argparse
from vigilo.common.gettext import translate, translate_narrow
_ = translate(__name__)
N_ = translate_narrow(__name__)

from vigilo.common.conf import settings
from vigilo.models.configure import configure_db
from vigilo.models import tables

__all__ = ('main', 'PrerequisitesError')

PERMISSIONS = {
    'ro': u'r',
    'rw': u'w',
}

REVERSE_PERMISSIONS = {
    # TRANSLATORS: Used in a sentence such as:
    # TRANSLATORS: '... permission on devices group "Foo"'.
    u'ro': _('Read-only'),

    # TRANSLATORS: Used in a sentence such as:
    # TRANSLATORS: '... permission on devices group "Foo"'.
    u'rw': _('Read/write'),
}

OBJECTS = {
    'devices': tables.SupItemGroup,
    'maps': tables.MapGroup,
    'graphs': tables.GraphGroup,
}

_COMMANDS = {}


class PrerequisitesError(Exception):
    pass


def _parse_args(args):
    """
    Analyse les paramètres passés à ce script et en déduit
    les options actives.

    @param args: Paramètres passés au script via la ligne de commandes.
    @type args: C{list}
    @return: Un tuple (options, arguments) avec le résultat de l'analyse.
    @rtype: C{tuple}
    """
    # Options générales.
    common_options = argparse.ArgumentParser()
    common_options.add_argument("-c", "--config", type=str,
        help=N_("Load configuration from this file."))

    # L'attribut "version" d'ArgumentParser est deprecated depuis argparse 1.1,
    # mais RHEL 6 utilise encore la version 1.0.1. On ignore l'avertissement.
    warnings.filterwarnings(
        "ignore",
        'The "version" argument to ArgumentParser is deprecated.*',
        DeprecationWarning
    )

    # Parser de plus haut niveau.
    dist = get_distribution('vigilo-models')
    # Pylint croit que "dist" est de type <str> ...
    #pylint: disable-msg=E1103
    parser = argparse.ArgumentParser(
        add_help=False,
        parents=[common_options],
        version="%%(prog)s %s" % dist.version,
    )

    subparser = parser.add_subparsers(metavar='', dest='action',
                                      title=N_('Subcommands'))
    actions = sorted(working_set.iter_entry_points("vigilo.cli"),
                     key=lambda x: x.name)
    for entry in actions:
        cls = entry.load()
        cmd_parser = subparser.add_parser(
            entry.name,
            add_help=False,
            parents=[common_options],
            help=cls.help,
        )
        cmd = cls(cmd_parser)
        # Définit s'il faut appeler transaction.commit() ou non.
        cmd_parser.set_defaults(commit=getattr(cls, 'commit', False))
        _COMMANDS[entry.name] = cmd

    return parser.parse_args(args)

def main():
    """
    Point d'entrée pour le script de réglage des permissions.
    """
    prepare_argparse()

    # Seul "root" (UID 0) est autorisé à administrer Vigilo.
    current_user = pwd.getpwuid(os.getuid())
    if current_user.pw_uid != 0:
        print(_("You must be root to use this script."))
        sys.exit(1)

    options = _parse_args(sys.argv[1:])

    if options.config:
        settings.load_file(options.config)
    else:
        settings.load_module(__name__)

    try:
        configure_db(settings['database'], 'sqlalchemy_')
    except KeyError:
        print(_('No database configuration found'))
        sys.exit(1)

    logger = get_logger(__name__)

    # On récupère la commande à exécuter et on appelle la fonction associée.
    try:
        _COMMANDS[options.action].execute(options, logger)
        if options.commit:
            transaction.commit()
        sys.exit(0)
    except PrerequisitesError:
        # Inutile d'afficher un message d'erreur ici,
        # les éventuelles erreurs sont directement tracées
        # par les commandes elles-mêmes.
        sys.exit(1)
