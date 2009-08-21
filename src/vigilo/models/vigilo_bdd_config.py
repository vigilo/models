# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
from __future__ import absolute_import

"""
BdD Vigilo Config
"""

from sqlalchemy.ext.declarative import declarative_base
from vigilo.common.conf import settings


__all__ = ('metadata', 'DeclarativeBase', 'bdd_basename', )


bdd_basename = settings['VIGILO_MODELS_BDD_BASENAME']
DeclarativeBase = declarative_base() # Not used, a shame
metadata = DeclarativeBase.metadata


