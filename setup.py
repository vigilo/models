#!/usr/bin/env python
# vim: set fileencoding=utf-8 sw=4 ts=4 et :
# Copyright (C) 2006-2018 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

import os, sys
from platform import python_version_tuple
from setuptools import setup, find_packages

sysconfdir = os.getenv("SYSCONFDIR", "/etc")

install_requires = [
    "Babel >= 0.9.4",
    "setuptools",
    "psycopg2",
    "SQLAlchemy >= 0.7.2",
    "SQLAlchemy < 1.0.0",
    "zope.sqlalchemy >= 0.4",
    "PasteDeploy",
    "vigilo-common",
    "transaction",
    "networkx",
    "passlib",
]
if tuple(python_version_tuple()) < ('2', '7'):
    install_requires.append("argparse")


tests_require = [
    'coverage',
    'nose',
    'pylint',
]

def install_i18n(i18ndir, destdir):
    data_files = []
    langs = []
    for f in os.listdir(i18ndir):
        if os.path.isdir(os.path.join(i18ndir, f)) and not f.startswith("."):
            langs.append(f)
    for lang in langs:
        for f in os.listdir(os.path.join(i18ndir, lang, "LC_MESSAGES")):
            if f.endswith(".mo"):
                data_files.append(
                        (os.path.join(destdir, lang, "LC_MESSAGES"),
                         [os.path.join(i18ndir, lang, "LC_MESSAGES", f)])
                )
    return data_files

setup(name='vigilo-models',
    version='4.1.0',
    author='Vigilo Team',
    author_email='contact.vigilo@c-s.fr',
    url='https://www.vigilo-nms.com/',
    license='http://www.gnu.org/licenses/gpl-2.0.html',
    description="Vigilo data models (ORM)",
    long_description="This library gives an API to the Vigilo data models.",
    zip_safe=False,
    install_requires=install_requires,
    extras_require={
        'tests': tests_require
    },
    message_extractors={
        'src': [
            ('**.py', 'python', None),
        ],
    },
    namespace_packages = [
        'vigilo',
    ],
    packages=find_packages("src"),
    package_data={
        'vigilo.models.migration': [
            '039_HLS_refactoring-export_hls.sh',
            '039_HLS_refactoring-export_hosts_hosttemplates.sh',
        ],
    },
    entry_points={
        'console_scripts': [
            'vigilo-updatedb = vigilo.models.websetup:init_db',
            'vigiboard-purge = vigilo.models.scripts.purge_vigiboard:main',
            'vigiboard-close = vigilo.models.scripts.close_vigiboard:main',
            'vigilo-passwd = vigilo.models.scripts.passwd:change_password',
            'vigilo-models-demo = vigilo.models.demo:run_demo',
            'vigilo-permissions = vigilo.models.scripts.permissions.main:main',
        ],
        # Compatibilité pour SQLAlchemy < 0.5.6 (RHEL 6),
        # où l'alias "postgresql" n'était pas encore défini.
        'sqlalchemy.databases': [
            'postgresql = sqlalchemy.databases.postgres:dialect',
        ],
    },
    package_dir={'': 'src'},
    data_files=install_i18n("i18n", os.path.join(sys.prefix, 'share', 'locale')) +
        [(os.path.join(sysconfdir, "vigilo/models"), ["deployment/settings.ini"])],
)
