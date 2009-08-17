# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""BdD Vigilo Config"""

from __future__ import absolute_import

from . import metadata, DeclarativeBase

from vigilo.common.conf import settings

__all__ = ('metadata', 'DeclarativeBase', 'bdd_basename', )

bdd_basename = settings['VIGILO_MODELS_BDD_BASENAME']

