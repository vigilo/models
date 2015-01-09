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

class TestVigiloPermissionsAddMap(unittest.TestCase):
    """Test l'ajout de permissions pour le type d'objet "map"."""
    _creator = fn.add_mapgroup
    _type = 'map'


    def setUp(self):
        """Initialisation du test."""
        setup_db()

        # Le groupe d'utilisateurs dont on va changer les permissions.
        self._usergroup = fn.add_usergroup(u"usergroup éçà")
        # Permet de vérifier qu'on ne donne pas TROP de permissions d'un coup.
        fn.add_usergroup(u"Foobars")

        # Pour éviter de binder "self" à la fonction.
        creator = self._creator.im_func
        root1 = creator(u"Root 1")
        root2 = creator(u"Root 2")
        # On définit 2 groupes avec le même nom mais des parents différents,
        # afin de vérifier le fonctionnement lorsque des correspondances
        # multiples sont trouvées.
        self._group1 = creator(u"group éçà", root1)
        self._group2 = creator(self._group1.name, root2)


    def tearDown(self):
        """Finalisation du test."""
        DBSession.expunge_all()
        transaction.abort()
        teardown_db()


    def shortDescription(self):
        """
        Permet d'inclure le type d'objet manipulé dans la description du test.
        """
        desc = super(TestVigiloPermissionsAddMap, self).shortDescription()
        if desc is None:
            desc = ""
        desc += " (%s)" % self._type
        return desc


    def test_add_single(self):
        """Ajout de permission sur un seul groupe."""
        for (incode, outcode) in commands._permissions.iteritems():
            print "Test permission %s" % incode
            options = NamespaceStub(
                permission=incode,
                object_type=self._type,
                usergroup=self._usergroup.group_name.encode('utf-8'),
                object_group=self._group1.path.encode('utf-8'),
                batch=False,
                update=False,
                commit=False,   # la base de test est en mémoire,
                                # en la committant, on perdrait tout.
            )
            res = commands.cmd_add(options)
            self.assertEquals(res, 0)

            # Une seule permission doit exister en base de données.
            # Elle doit porter sur le groupe 1 définis par le test
            # et avoir le bon type d'accès.
            dataperm = DBSession.query(tables.DataPermission).one()
            self.assertEquals(dataperm.idgroup, self._group1.idgroup)
            self.assertEquals(dataperm.idusergroup, self._usergroup.idgroup)
            self.assertEquals(dataperm.access, outcode)

            # Suppression de la permission pour le test
            # du type de permission suivant.
            DBSession.delete(dataperm)
            DBSession.flush()
            dataperm = DBSession.query(tables.DataPermission).first()
            self.assertEquals(dataperm, None)


    def test_add_multiple_error(self):
        """Pas de permission sur plusieurs groupes par défaut."""
        for incode in commands._permissions:
            print "Test permission %s" % incode
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
            res = commands.cmd_add(options)
            self.assertNotEquals(res, 0)

            # Aucune permission n'a été ajoutée.
            dataperm = DBSession.query(tables.DataPermission).first()
            self.assertEquals(dataperm, None)


    def test_add_multiple_batch(self):
        """Ajout permission sur plusieurs groupes en mode batch."""
        for (incode, outcode) in commands._permissions.iteritems():
            print "Test permission %s" % incode
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
            res = commands.cmd_add(options)
            self.assertEquals(res, 0)

            # 2 permissions doivent avoir été ajoutées.
            dataperms = DBSession.query(tables.DataPermission).all()
            self.assertEquals(2, len(dataperms))

            idgroups = [self._group1.idgroup, self._group2.idgroup]
            for dataperm in dataperms:
                self.assertTrue(dataperm.idgroup in idgroups)
                idgroups.remove(dataperm.idgroup)
                self.assertEquals(dataperm.idusergroup, self._usergroup.idgroup)
                self.assertEquals(dataperm.access, outcode)

            # Suppression des permissions pour le test
            # du type de permission suivant.
            for dataperm in dataperms:
                DBSession.delete(dataperm)
                DBSession.flush()
            dataperm = DBSession.query(tables.DataPermission).first()
            self.assertEquals(dataperm, None)


    def _add_permission(self, group, perm):
        print "group = %r, perm = %r" % (unicode(group).encode('utf-8'), perm)
        DBSession.add(tables.DataPermission(
            idgroup=group.idgroup,
            idusergroup=self._usergroup.idgroup,
            access=unicode(perm),
        ))
        DBSession.flush()


    def test_add_conflict(self):
        """Détection des conflits de permission."""
        for incode in commands._permissions:
            print "Test permission %s" % incode
            # On simule l'existence d'une permission avant le début du test.
            # Si le test porte sur la permission "lecture seule", alors la
            # permission existante est en lecture/écriture et vice-versa.
            existing_perm = (incode == "ro") and "w" or "r"
            self._add_permission(self._group1, existing_perm)

            options = NamespaceStub(
                permission=incode,
                object_type=self._type,
                usergroup=self._usergroup.group_name.encode('utf-8'),
                object_group=self._group1.path.encode('utf-8'),
                batch=False,
                update=False,
                commit=False,   # la base de test est en mémoire,
                                # en la committant, on perdrait tout.
            )
            # La demande doit être rejetée car elle rentre
            # en conflit avec les permissions existantes.
            res = commands.cmd_add(options)
            self.assertNotEquals(res, 0)

            # Une seule permission doit exister en base de données.
            dataperm = DBSession.query(tables.DataPermission).one()
            # Le contenu de la permission NE DOIT PAS avoir changé.
            self.assertEquals(self._usergroup.idgroup, dataperm.idusergroup)
            self.assertEquals(self._group1.idgroup, dataperm.idgroup)
            self.assertEquals(existing_perm, dataperm.access)

            # Suppression de la permission pour le test
            # du type de permission suivant.
            DBSession.delete(dataperm)
            DBSession.flush()
            DBSession.expunge_all() # Nécessaire pour éviter que l'ancienne
                                    # DataPerm ne soit "vue" à l'itération
                                    # suivante.
            dataperm = DBSession.query(tables.DataPermission).first()
            self.assertEquals(dataperm, None)


    def test_update(self):
        """Mise à jour des permissions."""
        for (incode, outcode) in commands._permissions.iteritems():
            print "Test permission %s" % incode
            # On simule l'existence d'une permission avant le début du test.
            # Si le test porte sur la permission "lecture seule", alors la
            # permission existante est en lecture/écriture et vice-versa.
            existing_perm = (incode == "ro") and "w" or "r"
            self._add_permission(self._group1, existing_perm)

            options = NamespaceStub(
                permission=incode,
                object_type=self._type,
                usergroup=self._usergroup.group_name.encode('utf-8'),
                object_group=self._group1.path.encode('utf-8'),
                batch=False,
                update=True,
                commit=False,   # la base de test est en mémoire,
                                # en la committant, on perdrait tout.
            )
            # La demande doit être rejetée car elle rentre
            # en conflit avec les permissions existantes.
            res = commands.cmd_add(options)
            self.assertEquals(res, 0)

            # Une seule permission doit exister en base de données.
            dataperm = DBSession.query(tables.DataPermission).one()
            # Le contenu de la permission doit avoir changé.
            self.assertEquals(self._usergroup.idgroup, dataperm.idusergroup)
            self.assertEquals(self._group1.idgroup, dataperm.idgroup)
            self.assertEquals(outcode, dataperm.access)

            # Suppression de la permission pour le test
            # du type de permission suivant.
            DBSession.delete(dataperm)
            DBSession.flush()
            DBSession.expunge_all() # Nécessaire pour éviter que l'ancienne
                                    # DataPerm ne soit "vue" à l'itération
                                    # suivante.
            dataperm = DBSession.query(tables.DataPermission).first()
            self.assertEquals(dataperm, None)




class TestVigiloPermissionsAddGraph(TestVigiloPermissionsAddMap):
    """Test l'ajout de permissions pour le type d'objet "graph"."""
    _creator = fn.add_graphgroup
    _type = 'graph'


class TestVigiloPermissionsAddSupItem(TestVigiloPermissionsAddMap):
    """Test l'ajout de permissions pour le type d'objet "monitored"."""
    _creator = fn.add_supitemgroup
    _type = 'monitored'
