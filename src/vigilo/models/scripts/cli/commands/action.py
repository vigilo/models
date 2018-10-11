# -*- coding: utf-8 -*-
# Copyright (C) 2018 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>
from __future__ import print_function

import json
from sqlalchemy.sql.expression import func
from vigilo.common import parse_path
from vigilo.models.scripts.cli.main import OBJECTS, PERMISSIONS, \
                                            REVERSE_PERMISSIONS,\
                                            PrerequisitesError
from vigilo.models.scripts.cli.commands import CommandBase
from vigilo.models.session import DBSession
from vigilo.models import tables

from vigilo.common.gettext import translate_narrow, translate
N_ = translate_narrow(__name__)
_ = translate(__name__)


class ActionCopy(CommandBase):
    help = N_("Copy a usergroup's rights to perform actions onto another group")

    def __init__(self, parser):
        parser.add_argument("source",
            help=N_("Usergroup whose rights will be copied."))
        parser.add_argument("target",
            help=N_("Usergroup whose rights will be overwritten."))

    def execute(self, options, logger):
        """
        Remplace les permissions sur les applications d'un groupe
        d'utilisateurs par celles d'un autre groupe.

        @param options: Options et arguments passés au script.
        @type options: C{argparse.Namespace}
        """

        # Validation des groupes d'utilisateurs.
        source = self._find_usergroup(options.source, logger)
        target = self._find_usergroup(options.target, logger)

        if source == target:
            logger.error(_("The source and target groups must be different"))
            raise PrerequisitesError(target)

        target.permissions = source.permissions
        DBSession.flush()


class ActionGrant(CommandBase):
    help = N_("Grant a usergroup the right to perform some action")

    def __init__(self, parser):
        parser.add_argument("usergroup",
            help=N_("Usergroup to act upon."))
        parser.add_argument("permission", nargs="+",
            help=N_("Permission to grant."))

    def execute(self, options, logger):
        """
        Ajoute des permissions sur les applications.

        @param options: Options et arguments passés au script.
        @type options: C{argparse.Namespace}
        """

        # Validation du groupe d'utilisateurs.
        usergroup = self._find_usergroup(options.usergroup, logger)

        # Récupération de la liste des permissions possibles.
        permissions = {}
        for permission in DBSession.query(
                tables.Permission
            ).order_by(tables.Permission.permission_name):
            permissions[permission.permission_name] = permission

        # Validation des permissions.
        current_permissions = usergroup.permissions
        for perm in options.permission:
            if perm not in permissions:
                logger.error(_('No such permission "%s"'), perm)
                raise PrerequisitesError(perm)

            permission = permissions[perm]
            if permission not in current_permissions:
                current_permissions.append(permission)

        usergroup.permissions = current_permissions
        DBSession.flush()


class ActionRevoke(CommandBase):
    help = N_("Revoke a usergroup's right to perform some action")

    def __init__(self, parser):
        parser.add_argument("usergroup",
            help=N_("Usergroup to act upon."))
        parser.add_argument("permission", nargs="+",
            help=N_("Permission to revoke."))

    def execute(self, options, logger):
        """
        Retire des permissions sur les applications.

        @param options: Options et arguments passés au script.
        @type options: C{argparse.Namespace}
        """

        # Validation du groupe d'utilisateurs.
        usergroup = self._find_usergroup(options.usergroup, logger)

        banned_permissions = [p.decode('utf-8') for p in options.permission]
        permissions = [p for p in usergroup.permissions
                       if p.permission_name not in banned_permissions]
        usergroup.permissions = permissions
        DBSession.flush()


class ActionList(CommandBase):
    help = N_("List possible actions")
    commit = False

    def __init__(self, parser):
        parser.add_argument("--format", choices=["text", "json", "pretty_json"],
            default="text", help=N_("Select the output format to use."))

    def execute(self, options, logger):
        objects = DBSession.query(tables.Permission.permission_name
            ).order_by(func.lower(tables.Permission.permission_name))
        output = [{"name": obj.permission_name} for obj in objects]

        if options.format in ('json', 'pretty_json'):
            indent = 2 if options.format == 'pretty_json' else None
            print(json.dumps(output, indent=indent))
        else:
            for entry in output:
                print("- %s" % (entry['name']))
