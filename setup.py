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
        author='Gabriel de Perthuis',
        author_email='gabriel.de-perthuis@c-s.fr',
        url='http://www.projet-vigilo.org/',
        description='vigilo models',
        license='http://www.gnu.org/licenses/gpl-2.0.html',
        long_description='Definition of the vigilo data model, db access.',
        zip_safe=False,
        install_requires=[
            'setuptools',
            'psycopg2',
            'SQLAlchemy',
            'zope.sqlalchemy',
            'vigilo-common',
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
            ]
        },
        package_dir={'': 'src'},
        )

