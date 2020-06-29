# -*- coding: utf-8 -*-
# Copyright (C) 2018-2020 CS GROUP – France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>
from __future__ import print_function

import json
from sqlalchemy.sql.expression import func
from vigilo.models.scripts.cli.main import REVERSE_PERMISSIONS, PrerequisitesError
from vigilo.models.scripts.cli.commands import CommandBase
from vigilo.models.session import DBSession
from vigilo.models import tables

from vigilo.common.gettext import translate_narrow, translate
N_ = translate_narrow(__name__)
_ = translate(__name__)


class UsergroupCreate(CommandBase):
    help = N_("Create a new usergroup")

    def __init__(self, parser):
        parser.add_argument("name", nargs="+",
            help=N_("Name for the new group."))

    def execute(self, options, logger):
        for groupname in options.name:
            groupname = groupname.decode('utf-8')
            group = tables.UserGroup.by_group_name(groupname)
            if not group:
                group = tables.UserGroup(group_name=groupname)
        DBSession.add(group)
        DBSession.flush()


class UsergroupDelete(CommandBase):
    help = N_("Delete some usergroup")

    def __init__(self, parser):
        parser.add_argument("name", nargs="+",
            help=N_("Name of the group to delete."))

    def execute(self, options, logger):
        names = [name.decode('utf-8') for name in options.name]
        DBSession.query(tables.UserGroup).filter(
            tables.UserGroup.group_name.in_(names)).delete(
            synchronize_session='fetch')
        DBSession.flush()


class UsergroupList(CommandBase):
    help = N_("List existing usergroups")
    commit = False

    def __init__(self, parser):
        parser.add_argument("--format", choices=["text", "json", "pretty_json"],
            default="text", help=N_("Select the output format to use."))

    def execute(self, options, logger):
        entries = DBSession.query(tables.UserGroup).order_by(
                    func.lower(tables.UserGroup.group_name))
        output = []
        for entry in entries:
            members = []
            for user in entry.users:
                members.append({
                    'login': user.user_name,
                    'fullname': user.fullname,
                    'email': user.email,
                })
            output.append({'name': entry.group_name, 'members': members})

        if options.format in ('json', 'pretty_json'):
            indent = 2 if options.format == 'pretty_json' else None
            print(json.dumps(output, indent=indent))
        else:
            for entry in output:
                members = [member['login'] for member in entry['members']]
                print("- %s (%s)" % (entry['name'], ', '.join(members)))


class UsergroupRename(CommandBase):
    help = N_("Rename a usergroup")

    def __init__(self, parser):
        parser.add_argument("old_name",
            help=N_("Current name of the group."))
        parser.add_argument("new_name",
            help=N_("New name for the group."))

    def execute(self, options, logger):
        old_group = self._find_usergroup(options.old_name, logger)
        new_group = tables.UserGroup.by_group_name(
                        options.new_name.decode('utf-8'))

        if new_group is not None:
            logger.error(_('A group named "%s" already exists'),
                        options.new_name)
            raise PrerequisitesError(options.new_name)

        old_group.group_name = options.new_name.decode('utf-8')
        DBSession.flush()


class UsergroupInclude(CommandBase):
    help = N_("Include users into a usergroup")

    def __init__(self, parser):
        parser.add_argument("usergroup",
            help=N_("Usergroup to act upon."))
        parser.add_argument("user", nargs="+",
            help=N_("User to include into the group."))

    def execute(self, options, logger):
        group = self._find_usergroup(options.usergroup, logger)

        users = []
        for username in options.user:
            user = self._find_user(username, logger)
            users.append(user)

        current_users = group.users
        for user in users:
            if user not in current_users:
                current_users.append(user)

        group.users = current_users;
        DBSession.flush()


class UsergroupExclude(CommandBase):
    help = N_("Exclude users from a usergroup")

    def __init__(self, parser):
        parser.add_argument("usergroup",
            help=N_("Usergroup to act upon."))
        parser.add_argument("user", nargs="+",
            help=N_("User to exclude from the group."))

    def execute(self, options, logger):
        group = self._find_usergroup(options.usergroup, logger)
        banned_users = [user.decode('utf-8') for user in options.user]
        new_users = [u for u in group.users if u.user_name not in banned_users]
        group.users = new_users;
        DBSession.flush()


class UsergroupShow(CommandBase):
    help = N_("Display various information about a group of users")
    commit = False

    def __init__(self, parser):
        parser.add_argument("usergroup",
            help=N_("Usergroup to act upon."))
        parser.add_argument("--format", choices=["text", "json", "pretty_json"],
            default="text", help=N_("Select the output format to use."))

    def execute(self, options, logger):
        group = self._find_usergroup(options.usergroup, logger)

        group_mapping = {
            tables.SupItemGroup: 'devices',
            tables.group.MapGroup: 'maps',
            tables.group.GraphGroup: 'graphs',
        }

        perm_mapping = {
            u'r': 'ro',
            u'w': 'rw',
        }

        data = []
        members = []
        actions = sorted([p.permission_name for p in group.permissions],
                         key=lambda p: p.lower())

        for user in group.users:
            members.append({
                'login': user.user_name,
                'fullname': user.fullname,
                'email': user.email,
            })

        for dataperm in group.datapermissions:
            permgroup = dataperm.group
            data.append({
                'access': perm_mapping[dataperm.access],
                'group': permgroup.path,
                'category': group_mapping[type(permgroup)],
            })

        output = {
            "name": group.group_name,
            "members": members,
            "actions": actions,
            "data": data,
        }

        if options.format in ('json', 'pretty_json'):
            indent = 2 if options.format == 'pretty_json' else None
            print(json.dumps(output, indent=indent))
        else:
            print(_("Group: %s") % (output['name'], ))

            print(_("Members:"))
            for member in output["members"]:
                print('- %(login)s ("%(fullname)s" <%(email)s>)' % member)

            print(_("Allowed actions:"))
            for action in output["actions"]:
                print("- %s" % (action, ))

            print(_("Data access:"))
            for action in output["data"]:
                print('- %(access)s permission on %(category)s '
                      'group "%(group)s"' % {
                            'access': REVERSE_PERMISSIONS[action['access']],
                            'category': action['category'],
                            'group': action['group'],
                      })

