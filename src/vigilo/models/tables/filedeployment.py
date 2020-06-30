# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2020 CS GROUP - France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Modèle pour la table FileDeployment.

Stocke le hash code d'un fichier déployé pour
implémenter la mise à jour différentielle
"""
from datetime import datetime
import hashlib

from sqlalchemy import Column
from sqlalchemy.types import Integer, Unicode, DateTime 

from vigilo.models.session import DeclarativeBase, DBSession

__all__ = ('FileDeployment', )

class FileDeployment(DeclarativeBase, object):
    """ Model used to implement partial deployment.
    """
    
    __tablename__ = 'vigilo_filedeployment'

    idfiledeployment = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    date = Column(
        DateTime(timezone=False),
        nullable=False,
    )
    
    hashcode = Column(Unicode(40), nullable=False)
    
    src_path = Column(Unicode(255), nullable=False)
    dest_path = Column(Unicode(255), nullable=False)

    def __init__(self, **kwargs):
        """
        Initialise l'instance avec les informations du fichier déployé.
        
        @param kwargs: Un dictionnaire avec les informations sur le fichier.
        @type kwargs: C{dict}
        """
        super(FileDeployment, self).__init__(**kwargs)
        
    def _get_actual_hashcode(self, sub_func=None):
        """
        Returns the hash code with
            - src_path
            - dest_path
            - file content

        @param sub_func: substitution function (to ignore rev changes)
        @type sub_func: C{function}
        """
        ob = hashlib.sha1(self.src_path)
        ob.update(self.dest_path)
        
        f = open(self.src_path, "rb")
        content = f.read()
        f.close()
        
        ob.update(content)
        
        return unicode(ob.hexdigest())
        
    def process_hashcode(self, sub_func=None):
        """ Updates the hashcode attribute.
        """
        self.hashcode = self._get_actual_hashcode(sub_func)
        self.date = datetime.utcnow()
        DBSession.flush()
        
    def need_deployment(self, sub_func=None):
        """ Returns True if deployment is needed
        """
        return (self.hashcode != self._get_actual_hashcode(sub_func))
    
    @classmethod
    def by_src_and_dest_pathes(cls, src_path, dest_path):
        """Renvoie une instance d'L{FileDeployment} à partir de son nom."""
        return DBSession.query(cls).filter(cls.src_path == src_path) \
                                   .filter(cls.dest_path == dest_path).first()
