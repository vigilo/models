# -*- coding: utf-8 -*-
# Copyright (C) 2018-2020 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>
from __future__ import print_function

import json
from sqlalchemy.sql.expression import func
from vigilo.models.scripts.cli.main import PrerequisitesError
from vigilo.models.scripts.cli.commands import CommandBase
from vigilo.models.session import DBSession
from vigilo.models import tables

from vigilo.common.gettext import translate_narrow, translate
N_ = translate_narrow(__name__)
_ = translate(__name__)


class UserList(CommandBase):
    help = N_("List existing users")
    commit = False

    def __init__(self, parser):
        parser.add_argument("--format", choices=["text", "json", "pretty_json"],
            default="text", help=N_("Select the output format to use."))

    def execute(self, options, logger):
        entries = DBSession.query(tables.User).order_by(
            func.lower(tables.User.user_name))
        output = []
        for entry in entries:
            groups = [g.group_name for g in entry.usergroups]
            output.append({
                'name': entry.user_name,
                'fullname': entry.fullname,
                'email': entry.email,
                'groups': groups,
            })

        if options.format in ('json', 'pretty_json'):
            indent = 2 if options.format == 'pretty_json' else None
            print(json.dumps(output, indent=indent))
        else:
            for entry in output:
                print('- %s ("%s" <%s>)' % (
                    entry['name'], entry['fullname'], entry['email']))


class UserCreate(CommandBase):
    help = N_("Create a new user")

    def __init__(self, parser):
        parser.add_argument("user",
            help=N_("Login for the new user."))
        parser.add_argument("--fullname", nargs=1, required=True,
            help=N_("Set the user's full name"))
        parser.add_argument("--email", nargs=1, required=True,
            help=N_("Set the user's email address"))
        parser.add_argument("--password", nargs=1, required=True,
            help=N_("Set the user's password"))

    def execute(self, options, logger):
        new_user = tables.User.by_user_name(options.user.decode('utf-8'))
        if new_user is not None:
            logger.error(_('A user already exists with this login'))
            raise PrerequisitesError(options.user)


        new_email = tables.User.by_email_address(
                        options.email[0].decode('utf-8'))
        if new_email is not None:
            logger.error(_('A user already exists with this email address'))
            raise PrerequisitesError(options.email[0])

        user = tables.User(
            user_name=options.user.decode('utf-8'),
            email=options.email[0].decode('utf-8'),
            fullname=options.fullname[0].decode('utf-8'),
            password=options.password[0].decode('utf-8'),
        )
        DBSession.add(user)
        DBSession.flush()


class UserDelete(CommandBase):
    help = N_("Delete some user")

    def __init__(self, parser):
        parser.add_argument("login", nargs="+",
            help=N_("Login of the user to delete."))

    def execute(self, options, logger):
        names = [name.decode('utf-8') for name in options.login]
        DBSession.query(tables.User).filter(
            tables.User.user_name.in_(names)).delete(
            synchronize_session='fetch')
        DBSession.flush()


class UserUpdate(CommandBase):
    help = N_("Update some user")

    def __init__(self, parser):
        parser.add_argument("user",
            help=N_("Login of the user to update."))
        parser.add_argument("--login", nargs=1, default=None,
            help=N_("Set the user's login name"))
        parser.add_argument("--fullname", nargs=1, default=None,
            help=N_("Set the user's full name"))
        parser.add_argument("--email", nargs=1, default=None,
            help=N_("Set the user's email address"))
        parser.add_argument("--password", nargs=1, default=None,
            help=N_("Set the user's password"))

    def execute(self, options, logger):
        user = self._find_user(options.user, logger)

        if options.login:
            new_user = tables.User.by_user_name(
                options.login[0].decode('utf-8'))
            if new_user is not None:
                logger.error(_('A user named "%s" already exists'),
                            options.login[0])
                raise PrerequisitesError(options.login[0])
            user.user_name = options.login[0].decode('utf-8')

        if options.email:
            new_email = tables.User.by_email_address(
                options.email[0].decode('utf-8'))
            if new_email is not None:
                logger.error(_('A user already exists with this email address'))
                raise PrerequisitesError(options.email[0])
            user.email = options.email[0].decode('utf-8')

        if options.fullname:
            user.fullname = options.fullname[0].decode('utf-8')

        if options.password:
            user.password = options.password[0].decode('utf-8')

        DBSession.flush()
