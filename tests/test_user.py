# -*- coding: utf-8 -*-
"""Test suite for User class"""
from nose.tools import eq_

from vigilo.models.tables import User, SupItemGroup, Permission, UserGroup,\
                                MapGroup, Map, DataPermission
from vigilo.models.session import DBSession

from controller import ModelTest

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

        root = SupItemGroup(name=u'root')
        DBSession.add(root)
        sub1 = SupItemGroup(name=u'sub1', parent=root)
        DBSession.add(sub1)
        sub2 = SupItemGroup(name=u'sub2', parent=sub1)
        DBSession.add(sub2)
        DBSession.flush()

        perm = Permission(permission_name=u'manage')
        perm.usergroups.append(usergroup)
        DBSession.flush()

        dataperm = DataPermission(
            usergroup=usergroup,
            group=sub2,
            access=u'r',
        )
        DBSession.add(dataperm)
        DBSession.flush()

        dataperm = DataPermission(
            usergroup=usergroup,
            group=root,
            access=u'r',
        )
        DBSession.add(dataperm)
        DBSession.flush()

        eq_([
                (root.idgroup, True),
                (sub1.idgroup, False),
                (sub2.idgroup, True),
            ], user.supitemgroups())
        
    def test_mapgroups(self):
        """Récupération des groupes de cartes accessibles"""
        user = User(user_name=u'manager', email=u'', fullname=u'')
        DBSession.flush()
        
        usergroup = UserGroup(group_name=u'managers')
        usergroup.users.append(user)
        DBSession.flush()

        g1 = MapGroup(name=u'groupe 1')
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
        
        
        eq_([g1.idgroup, g11.idgroup, g111.idgroup],
            user.mapgroups(True))

        eq_([g111],
            user.mapgroups(False, True))

