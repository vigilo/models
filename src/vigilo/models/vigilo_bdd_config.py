# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""
Configuration des métadonnées concernant la base de données
de Vigilo, utilisée par SQLAlchemy.
"""

from sqlalchemy.ext.declarative import declarative_base
from vigilo.common.conf import settings

__all__ = ('metadata', 'DeclarativeBase', 'bdd_basename', )

bdd_basename = settings['VIGILO_MODELS_BDD_BASENAME']
DeclarativeBase = declarative_base()
metadata = DeclarativeBase.metadata

