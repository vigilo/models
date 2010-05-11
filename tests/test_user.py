# -*- coding: utf-8 -*-
"""Test suite for User class"""
from nose.tools import eq_

from vigilo.models.tables import User, SupItemGroup, Permission, UserGroup,\
                                MapGroup
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

        root = SupItemGroup.create(u'root')
        sub1 = SupItemGroup.create(u'sub1', parent=root)
        sub2 = SupItemGroup.create(u'sub2', parent=sub1)
        sub3 = SupItemGroup.create(u'sub3', parent=sub2)
        sub4 = SupItemGroup.create(u'sub4', parent=sub3)

        perm = Permission(permission_name=u'manage')
        perm.usergroups.append(usergroup)
        perm.supitemgroups.append(sub2)
        DBSession.flush()

        eq_([sub2.idgroup, sub3.idgroup, sub4.idgroup],
            user.supitemgroups(False))
        eq_([root.idgroup, sub1.idgroup, sub2.idgroup],
            user.supitemgroups(True))
        
    def test_mapgroups(self):
        """Récupération des groupes de cartes accessibles"""
        user = User(user_name=u'manager', email=u'', fullname=u'')
        DBSession.flush()
        
        usergroup = UserGroup(group_name=u'managers')
        usergroup.users.append(user)
        DBSession.flush()
        
        g1 = MapGroup.create(u'groupe 1')
        g11 = MapGroup.create(u'groupe 1.1', parent=g1)
        g111 = MapGroup.create(u'groupe 1.1.1', parent=g11)
        g1111 = MapGroup.create(u'groupe 1.1.1.1', parent=g111)
        
        perm = Permission(permission_name=u'manage')
        perm.usergroups.append(usergroup)
        perm.mapgroups.append(g111)
        DBSession.flush()
        
        print "user.mapgroups(True)",user.mapgroups(True)
        print "g111.idgroup", g111.idgroup
        
        eq_([g111.idgroup, g1111.idgroup],
            user.mapgroups(True))
        
        eq_([g111, g1111],
            user.mapgroups(False))
        
        

