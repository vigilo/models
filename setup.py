#!/usr/bin/env python
# vim: set fileencoding=utf-8 sw=4 ts=4 et :
from setuptools import setup

tests_require = [
    'coverage',
    'nose',
    'pylint',
]

setup(name='vigilo-models',
    version='0.1',
    author='Vigilo Team',
    author_email='contact@projet-vigilo.org',
    url='http://www.projet-vigilo.org/',
    description='vigilo models',
    license='http://www.gnu.org/licenses/gpl-2.0.html',
    long_description='Definition of the Vigilo data model.',
    zip_safe=False,
    install_requires=[
        "setuptools",
        "psycopg2",
        "SQLAlchemy",
        "zope.sqlalchemy >= 0.4",
        "PasteScript >= 1.7", # setup_requires has issues
        "vigilo-common",
    ],
    extras_require ={
        'tests': tests_require
    },
    namespace_packages = [
        'vigilo',
    ],
    packages=[
        'vigilo',
        'vigilo.models',
    ],
    entry_points={
        'console_scripts': [
            'vigilo-models-init-db = vigilo.models.websetup:init_db',
        ],
    },
    package_dir={'': 'src'},
#    data_files=[
#        ('/etc/vigilo/models/', [
#            'deployment/settings.ini',
#        ]),
#    ],
)

