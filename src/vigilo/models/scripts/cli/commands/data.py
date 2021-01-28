# -*- coding: utf-8 -*-
# Copyright (C) 2018-2021 CS GROUP - France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>
from __future__ import print_function

import json
from sqlalchemy.sql.expression import func
from vigilo.common import parse_path
from vigilo.models.scripts.cli.main import OBJECTS, PERMISSIONS, PrerequisitesError
from vigilo.models.scripts.cli.commands import CommandBase
from vigilo.models.session import DBSession
from vigilo.models import tables

from vigilo.common.gettext import translate_narrow, translate
N_ = translate_narrow(__name__)
_ = translate(__name__)


class DataCopy(CommandBase):
    help = N_("Copy a usergroup's rights to act on data onto another group")

    def __init__(self, parser):
        parser.add_argument("source",
            help=N_("Usergroup whose rights will be copied."))
        parser.add_argument("target",
            help=N_("Usergroup whose rights will be overwritten."))

    def execute(self, options, logger):
        """
        Remplace les permissions sur les données d'un groupe
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

        DBSession.query(
                tables.DataPermission
            ).filter(tables.DataPermission.idusergroup == target.idgroup
            ).delete(synchronize_session=False)

        for dataperm in source.datapermissions:
            DBSession.add(tables.DataPermission(
                idusergroup=target.idgroup,
                idgroup=dataperm.idgroup,
                access=dataperm.access,
            ))
        DBSession.flush()


class DataGrant(CommandBase):
    help = N_("Grant a usergroup the right to act on some data")

    def __init__(self, parser):
        parser.add_argument("usergroup",
            help=N_("Usergroup to act upon."))
        parser.add_argument("permission",
            choices=["ro", "rw"],
            help=N_("Type of permission to give: 'ro' (%(ro)s) "
                    "or 'rw' (%(rw)s).") % {
                        'ro': N_('read-only'),
                        'rw': N_('read/write'),
                    })
        parser.add_argument(
            "object_type",
            choices=["devices", "maps", "graphs"],
            help=N_("Type of object to act upon: "
                    "'devices' for groups of monitored items, "
                    "'maps' for groups of maps, "
                    "or 'graphs' for groups of graphs"))
        parser.add_argument("object_group", nargs="+",
            help=N_("Full path to the object group to act upon."))

    def execute(self, options, logger):
        """
        Change les permissions d'un groupe d'utilisateurs
        vis-à-vis d'un groupe d'objets.

        @param options: Options et arguments passés au script.
        @type options: C{argparse.Namespace}
        """
        permission = PERMISSIONS[options.permission]
        object_type = OBJECTS[options.object_type]

        # Vérifications sur le groupe d'utilisateurs.
        usergroup = self._find_usergroup(options.usergroup, logger)

        # Vérifications sur le chemin des groupes d'objets.
        groups = []
        for group_path in options.object_group:
            group = self._find_objgroup(object_type, group_path, logger)
            groups.append(group)

        datapermissions = {}
        for dataperm in usergroup.datapermissions:
            datapermissions[dataperm.idgroup] = dataperm

        for group in groups:
            # Mise à jour des permissions si une entrée existe déjà.
            if group.idgroup in datapermissions:
                datapermissions[group.idgroup].access = permission

            # Sinon, on ajoute la nouvelle permission.
            else:
                datapermissions[group.idgroup] = tables.DataPermission(
                    idusergroup=usergroup.idgroup,
                    idgroup=group.idgroup,
                    access=permission,
                )

            # Ajout de l'object créé ou mis à jour à la session,
            # afin de sauvegarder son état lors du prochain flush().
            DBSession.add(datapermissions[group.idgroup])
        DBSession.flush()


class DataRevoke(CommandBase):
    help = N_("Revoke a usergroup's right to act on some data")

    def __init__(self, parser):
        parser.add_argument("usergroup",
            help=N_("Usergroup to act upon."))
        parser.add_argument(
            "object_type",
            choices=["devices", "maps", "graphs"],
            help=N_("Type of object to act upon: "
                    "'devices' for groups of monitored items, "
                    "'maps' for groups of maps, "
                    "or 'graphs' for groups of graphs"))
        parser.add_argument("object_group", nargs="+",
            help=N_("Full path to the object group to act upon."))

    def execute(self, options, logger):
        """
        Supprime les permissions d'un groupe d'utilisateurs
        vis-à-vis d'un groupe d'objets.

        @param options: Options et arguments passés au script.
        @type options: C{argparse.Namespace}
        @return: Code de sortie (0 = pas d'erreur, autre = erreur).
        @rtype: C{int}
        """
        object_type = OBJECTS[options.object_type]

        # Vérifications sur le groupe d'utilisateurs.
        usergroup = self._find_usergroup(options.usergroup, logger)

        # Vérifications sur le chemin des groupes d'objets.
        groups = []
        for group_path in options.object_group:
            group = self._find_objgroup(object_type, group_path, logger)
            groups.append(group)

        idgroups = [group.idgroup for group in groups]
        for dataperm in usergroup.datapermissions:
            # Si le groupe sur lequel porte la permission
            # ne fait pas partie des groupes visés, on l'ignore.
            if dataperm.idgroup not in idgroups:
                continue

            # Sinon, on procède à la suppression de la permission.
            DBSession.delete(dataperm)
        DBSession.flush()


class DataList(CommandBase):
    help = N_("List available groups of objects")
    commit = False

    def __init__(self, parser):
        parser.add_argument(
            "object_type",
            choices=["devices", "maps", "graphs"],
            help=N_("Objects to display: "
                    "'devices' for groups of monitored items, "
                    "'maps' for groups of maps, "
                    "or 'graphs' for groups of graphs"))
        parser.add_argument("--format", choices=["text", "json", "pretty_json"],
            default="text", help=N_("Select the output format to use."))

    def execute(self, options, logger):
        object_type = OBJECTS[options.object_type]

        # ATTENTION : Le filter() devrait être superflu, mais il ne l'est pas !
        objects = DBSession.query(tables.GroupPath.path
            ).join(
                (object_type, object_type.idgroup == tables.GroupPath.idgroup),
            ).filter(object_type.grouptype ==
                object_type.__mapper_args__['polymorphic_identity']
            ).order_by(func.lower(tables.GroupPath.path))
        output = [{"name": obj.path} for obj in objects]

        if options.format in ('json', 'pretty_json'):
            indent = 2 if options.format == 'pretty_json' else None
            print(json.dumps(output, indent=indent))
        else:
            for entry in output:
                print("- %s" % (entry['name']))

