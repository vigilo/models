# -*- coding: utf-8 -*-
# Copyright (C) 2011-2015 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Tests du script de gestion des permissions."""

# pylint: disable-msg=C0111,W0613,R0904,W0212
# - C0111: Missing docstring
# - W0613: Unused argument
# - R0904: Too many public methods
# - W0212: Access to a protected member of a client class

import unittest
import transaction

from vigilo.models.test.controller import setup_db, teardown_db

from vigilo.models.scripts.permissions import commands
from vigilo.models import tables
from vigilo.models.demo import functions as fn
from vigilo.models.session import DBSession

from vigilo.common.logging import get_logger
LOGGER = get_logger(__name__)

class NamespaceStub(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class TestVigiloPermissionsRemoveMap(unittest.TestCase):
    """Test la suppression de permissions pour le type d'objet "map"."""
    _creator = fn.add_mapgroup
    _type = 'map'


    def setUp(self):
        """Initialisation du test."""
        setup_db()

        # Le groupe d'utilisateurs dont on va changer les permissions.
        self._usergroup = fn.add_usergroup(u"usergroup éçà")
        # Permet de vérifier qu'on ne retire pas TROP de permissions d'un coup.
        self._foobars = fn.add_usergroup(u"Foobars")

        # Pour éviter de binder "self" à la fonction.
        creator = self._creator.im_func
        root1 = creator(u"Root 1")
        root2 = creator(u"Root 2")
        root3 = creator(u"Root 3")
        root4 = creator(u"Root 4")
        # On définit 4 groupes avec des noms qui se recoupent.
        self._group1 = creator(u"group éçà", root1)
        self._group2 = creator(self._group1.name, root2)
        self._group3 = creator(self._group1.name, root3)
        self._group4 = creator(self._group1.name, root4)


    def tearDown(self):
        """Finalisation du test."""
        DBSession.expunge_all()
        transaction.abort()
        teardown_db()


    def shortDescription(self):
        """
        Permet d'inclure le type d'objet manipulé dans la description du test.
        """
        desc = super(TestVigiloPermissionsRemoveMap, self).shortDescription()
        if desc is None:
            desc = ""
        desc += " (%s)" % self._type
        return desc


    def _set_permissions(self):
        # Affectation de permissions sur les différents groupes.
        perms = {
            self._group1: u'r',
            self._group2: u'r',
            self._group3: u'w',
            self._group4: u'w',
        }
        for (group, perm) in perms.iteritems():
            DBSession.add(tables.DataPermission(
                idgroup=group.idgroup,
                idusergroup=self._usergroup.idgroup,
                access=perm,
            ))
            DBSession.add(tables.DataPermission(
                idgroup=group.idgroup,
                idusergroup=self._foobars.idgroup,
                access=perm,
            ))
        DBSession.flush()


    def test_remove_permission_single(self):
        """Retrait de permission sur un seul groupe."""
        # Permettra de tester une tentative de suppression
        # sur le group3, en ignorant l'accès actuel.
        permissions = commands._permissions.copy()
        permissions[None] = None
        for incode in commands._permissions:
            print "Test permission %s" % incode
            self._set_permissions()
            if incode == "ro":
                group = self._group1
            else:
                group = self._group3

            options = NamespaceStub(
                permission=incode,
                object_type=self._type,
                usergroup=self._usergroup.group_name.encode('utf-8'),
                object_group=group.path.encode('utf-8'),
                batch=False,
                update=False,
                commit=False,   # la base de test est en mémoire,
                                # en la committant, on perdrait tout.
            )
            res = commands.cmd_remove(options)
            self.assertEquals(res, 0)

            # On doit avoir 7 permissions en base :
            # les 8 de départ - 1 permission supprimée.
            dataperms = DBSession.query(tables.DataPermission).all()
            self.assertEquals(7, len(dataperms))

            # On vérifie que la permission qu'on voulait supprimer
            # a effectivement été supprimée.
            dataperm = DBSession.query(tables.DataPermission
                ).filter(tables.DataPermission.idgroup == group.idgroup
                ).filter(tables.DataPermission.idusergroup ==
                    self._usergroup.idgroup
                ).first()
            self.assertEquals(None, dataperm)

            # Suppression des permissions pour le test
            # du type de permission suivant.
            for dataperm in DBSession.query(tables.DataPermission).all():
                DBSession.delete(dataperm)
            DBSession.flush()
            dataperm = DBSession.query(tables.DataPermission).first()
            self.assertEquals(dataperm, None)


    def test_remove_multiple_error(self):
        """Pas de retrait de permissions sur plusieurs groupes par défaut."""
        # Permettra de tester une tentative de suppression
        # de toutes les permissions, quelle que soit le type.
        permissions = commands._permissions.copy()
        permissions[None] = None
        for incode in permissions:
            print "Test permission %r" % (incode, )
            self._set_permissions()

            options = NamespaceStub(
                permission=incode,
                object_type=self._type,
                usergroup=self._usergroup.group_name.encode('utf-8'),
                object_group=self._group1.name.encode('utf-8'),
                batch=False,
                update=False,
                commit=False,   # la base de test est en mémoire,
                                # en la committant, on perdrait tout.
            )

            # La commande a été rejetée.
            res = commands.cmd_remove(options)
            self.assertNotEquals(res, 0)

            # Aucune permission n'a été retirée.
            dataperms = DBSession.query(tables.DataPermission).all()
            self.assertEquals(8, len(dataperms))

            # Suppression des permissions pour le test
            # du type de permission suivant.
            for dataperm in DBSession.query(tables.DataPermission).all():
                DBSession.delete(dataperm)
            DBSession.flush()
            dataperm = DBSession.query(tables.DataPermission).first()
            self.assertEquals(dataperm, None)


    def test_remove_multiple_batch(self):
        """Retrait de permissions sur plusieurs groupes en mode batch."""
        # Permettra de tester une tentative de suppression
        # de toutes les permissions, quelle que soit le type.
        permissions = commands._permissions.copy()
        permissions[None] = None
        for incode in permissions:
            print "Test permission %s" % incode
            self._set_permissions()
            options = NamespaceStub(
                permission=incode,
                object_type=self._type,
                usergroup=self._usergroup.group_name.encode('utf-8'),
                object_group=self._group1.name.encode('utf-8'),
                batch=True,
                update=False,
                commit=False,   # la base de test est en mémoire,
                                # en la committant, on perdrait tout.
            )
            res = commands.cmd_remove(options)
            self.assertEquals(res, 0)

            dataperms = DBSession.query(tables.DataPermission).all()

            if incode is None:
                # Les 4 permissions de l'utilisateur
                # doivent avoir été supprimées.
                # Il reste donc 8-4 permissions en base.
                self.assertEquals(4, len(dataperms))
            else:
                # 2 permissions de l'utilisateur doivent avoir été supprimées.
                # Il en reste donc 8-2 en base.
                self.assertEquals(6, len(dataperms))

            # Suppression des permissions pour le test
            # du type de permission suivant.
            for dataperm in dataperms:
                DBSession.delete(dataperm)
                DBSession.flush()
            dataperm = DBSession.query(tables.DataPermission).first()
            self.assertEquals(dataperm, None)


class TestVigiloPermissionsRemoveGraph(TestVigiloPermissionsRemoveMap):
    """Test la suppression de permissions pour le type d'objet "graph"."""
    _creator = fn.add_graphgroup
    _type = 'graph'


class TestVigiloPermissionsRemoveSupItem(TestVigiloPermissionsRemoveMap):
    """Test la suppression de permissions pour le type d'objet "monitored"."""
    _creator = fn.add_supitemgroup
    _type = 'monitored'
