# -*- coding: utf-8 -*-
"""Test suite for ServiceGroup class"""
import os
import tempfile
import shutil
from datetime import datetime
import hashlib

from nose.tools import assert_equal

from vigilo.models.session import DBSession
from vigilo.models.tables import FileDeployment
from controller import ModelTest


class TestFileDeployment(ModelTest):
    tmpdir = None
    klass = FileDeployment
    attrs = {
        'hashcode': u'-',
        'date': datetime.now(),
        'src_path': u'',
        'dest_path': u'sample_dep.dest',
    }

    def setup(self):
        """Call before every test case."""
        # Prepare temporary directory
        self.tmpdir = tempfile.mkdtemp()
        # move src file in the tmp dir
        self.attrs['src_path'] = os.path.join(self.tmpdir, u'sample_dep.src')
        # build a sample file
        f = open(self.attrs['src_path'], 'w')
        f.write("this is a sample file to deploy")
        f.close()
        
        super(TestFileDeployment, self).setup()

    def tearDown(self):
        """Tear down the fixture used to test the model."""
        super(TestFileDeployment, self).tearDown()
        shutil.rmtree(self.tmpdir)

    def test_filedeployment(self):
        """Checks the filedeployment object."""
        obj = DBSession.query(self.klass).one()
        obj.process_hashcode()
        DBSession.flush()
        
        # checks the hashcode
        shaob = hashlib.sha1(os.path.join(self.tmpdir, u'sample_dep.src'))
        shaob.update('sample_dep.dest')
        shaob.update("this is a sample file to deploy")
        
        assert_equal(u'' + shaob.hexdigest(), obj.hashcode)
