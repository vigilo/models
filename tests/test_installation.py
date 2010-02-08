# -*- coding: utf-8 -*-
"""Test suite for Installation class"""
from vigilo.models import VigiloServer, Installation, Application
from vigilo.models.configure import DBSession

from controller import ModelTest

class TestInstallation(ModelTest):


    klass = Installation
    attrs = {
        'jid': u'foo@bar.baz',
    }

    def do_get_dependencies(self):
        """Generate some data for the test"""
        vserver = VigiloServer(
           name=u'supserver1',
           description=u'a vigilo server'
        )
        DBSession.add(vserver)

        app = Application(
           name=u'app',
        )
        DBSession.add(app)

        DBSession.flush()
        return dict(
            vigiloserver=DBSession.query(VigiloServer).first(),
            application=DBSession.query(Application).first()
        )

    def __init__(self):
        ModelTest.__init__(self)

