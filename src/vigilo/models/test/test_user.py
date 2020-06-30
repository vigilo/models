# -*- coding: utf-8 -*-
# Copyright (C) 2006-2020 CS GROUP - France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for User class"""

# pylint: disable-msg=C0111,W0613,R0904,W0212
# - C0111: Missing docstring
# - W0613: Unused argument
# - R0904: Too many public methods
# - W0212: Access to a protected member of a client class

import hashlib
from nose.tools import eq_

from vigilo.models.tables import User, SupItemGroup, Permission, UserGroup, \
                                MapGroup, DataPermission
from vigilo.models.session import DBSession

from vigilo.models.test.controller import ModelTest

class TestUser(ModelTest):
    """Unit test case for the ``User`` model."""

    klass = User
    attrs = dict(
        user_name = u"foobar",
        email = u"foobar@example.org",
        fullname = u'Foo bar',
    )

    def __init__(self):
        """Initialisation du test."""
        ModelTest.__init__(self)

    def test_no_permissions_by_default(self):
        """User objects should have no permission by default."""
        eq_(len(self.obj.permissions), 0)

    def test_getting_by_email(self):
        """Users should be fetcheable by their email"""
        him = User.by_email_address(u"foobar@example.org")
        eq_(him, self.obj)

    def test_getting_by_user_name(self):
        """Users should be fetcheable by their username"""
        him = User.by_user_name(u"foobar")
        eq_(him, self.obj)

    def test_get_supitemgroups(self):
        """Récupération des groupes d'éléments supervisés accessibles."""
        user = User(user_name=u'manager', email=u'', fullname=u'')
        DBSession.flush()

        usergroup = UserGroup(group_name=u'managers')
        usergroup.users.append(user)
        DBSession.flush()

        root = SupItemGroup(name=u'root', parent=None)
        DBSession.add(root)
        sub1 = SupItemGroup(name=u'sub1', parent=root)
        DBSession.add(sub1)
        sub2 = SupItemGroup(name=u'sub2', parent=root)
        DBSession.add(sub2)
        sub21 = SupItemGroup(name=u'sub21', parent=sub2)
        DBSession.add(sub21)
        DBSession.flush()

        dataperm = DataPermission(
            usergroup=usergroup,
            group=sub2,
            access=u'r',
        )
        DBSession.add(dataperm)
        DBSession.flush()

        eq_([
                (root.idgroup, False),
                (sub2.idgroup, True),
                (sub21.idgroup, True),
            ], user.supitemgroups())

    def test_mapgroups(self):
        """Récupération des groupes de cartes accessibles"""
        user = User(user_name=u'manager', email=u'', fullname=u'')
        DBSession.flush()

        usergroup = UserGroup(group_name=u'managers')
        usergroup.users.append(user)
        DBSession.flush()

        g1 = MapGroup(name=u'groupe 1', parent=None)
        DBSession.add(g1)
        g11 = MapGroup(name=u'groupe 1.1', parent=g1)
        DBSession.add(g11)
        g111 = MapGroup(name=u'groupe 1.1.1', parent=g11)
        DBSession.add(g111)
        g1111 = MapGroup(name=u'groupe 1.1.1.1', parent=g111)
        DBSession.add(g1111)
        DBSession.flush()

        perm = Permission(permission_name=u'manage')
        DBSession.add(perm)
        perm.usergroups.append(usergroup)
        DBSession.flush()

        dataperm = DataPermission(
            idusergroup=usergroup.idgroup,
            idgroup=g111.idgroup,
            access=u'r',
        )
        DBSession.add(dataperm)
        DBSession.flush()

        # g1111 est considéré comme un groupe direct par mapgroups()
        # car l'accès est autorisé récursivement.
        expected = sorted([
            g1.idgroup,
            g11.idgroup,
            g111.idgroup,
            g1111.idgroup,
        ])
        received = sorted(user.mapgroups(True))
        eq_(expected, received)

        expected = sorted([g111, g1111])
        received = sorted(user.mapgroups(False, True))
        eq_(expected, received)

    def test_hash_function(self):
        """Hachage des mots de passe (accentués)."""
        from vigilo.models import configure
        configure.SCHEMES = ['hex_md5']
        configure.DEPRECATED_SCHEMES = []
        password = u'éàçù'
        self.obj.password = password
        DBSession.flush()

        digest = hashlib.md5(password.encode('utf-8')
                    ).hexdigest().decode('utf-8')
        user = DBSession.query(User).filter(User._password == digest).one()
        eq_(user, self.obj)

