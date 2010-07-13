#!/usr/bin/env python
# vim: set fileencoding=utf-8 sw=4 ts=4 et :
import os, sys
from setuptools import setup, find_packages

sysconfdir = os.getenv("SYSCONFDIR", "/etc")

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
    version='2.0.0',
    author='Vigilo Team',
    author_email='contact@projet-vigilo.org',
    url='http://www.projet-vigilo.org/',
    description='vigilo models',
    license='http://www.gnu.org/licenses/gpl-2.0.html',
    long_description='Definition of the Vigilo data model.',
    zip_safe=False,
    install_requires=[
        "Babel >= 0.9.4",
        "setuptools",
        "psycopg2",
        "SQLAlchemy",
        "zope.sqlalchemy >= 0.4",
        "PasteScript >= 1.7", # setup_requires has issues
        "vigilo-common",
        "transaction",
    ],
    extras_require ={
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
    entry_points={
        'console_scripts': [
            'vigilo-models-init-db = vigilo.models.websetup:init_db',
            'vigilo-models-clean-vigiboard = vigilo.models.websetup:clean_vigiboard',
            'vigilo-models-demo = vigilo.models.demo:run_demo',
        ],
    },
    package_dir={'': 'src'},
    data_files=install_i18n("i18n", os.path.join(sys.prefix, 'share', 'locale')) +
        [(os.path.join(sysconfdir, "vigilo/models"), ["deployment/settings.ini"])],
)

