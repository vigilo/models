# -*- coding: utf-8 -*-
"""Test suite for ServiceGroup class"""
import os
import tempfile
import shutil

from datetime import datetime

from nose.tools import assert_equal

from vigilo.models import FileDeployment
from .controller import ModelTest
from vigilo.models.session import DBSession

import hashlib

class TestFileDeployment(ModelTest):
    
    def setup(self):
        """Call before every test case."""
        # Prepare temporary directory
        self.tmpdir = tempfile.mkdtemp()
        # move src file in the tmp dir
        self.attrs['src_path'] = os.path.join(self.tmpdir, self.attrs['src_path'])
        # build a sample file
        f = open(self.attrs['src_path'], 'w')
        f.write("this is a sample file to deploy")
        f.close()
        
        super(TestFileDeployment, self).setup()

    def tearDown(self):
        """Tear down the fixture used to test the model."""
        super(TestFileDeployment, self).tearDown()
        #shutil.rmtree(self.tmpdir)

    tmpdir = None
    klass = FileDeployment
    attrs = {
        'hashcode': u'-',
        'date': datetime.now(),
        'src_path': u'sample_dep.src',
        'dest_path': u'sample_dep.dest'
    }
    
    def __init__(self):
        ModelTest.__init__(self)
    
    def test_filedeployment(self):
        """Checks the filedeployment object."""
        obj = DBSession.query(self.klass).one()
        obj.process_hashcode()
        DBSession.flush()
        
        # checks the hashcode
        shaob = hashlib.sha1(os.path.join(self.tmpdir, self.attrs['src_path']))
        shaob.update('sample_dep.dest')
        shaob.update("this is a sample file to deploy")
        
        assert_equal(shaob.hexdigest(), obj.hashcode)
        
        # TODO: should be put in tearDown; bug ?
        shutil.rmtree(self.tmpdir)

