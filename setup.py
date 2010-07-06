#!/usr/bin/env python
# vim: set fileencoding=utf-8 sw=4 ts=4 et :
import os
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
        "decorator",
        "TurboJson >= 1.2",
        "prioritized-methods >= 0.2.1",
        "FormEncode >= 1.1",
        "WebFlash >=0.1a7",
        "PEAK-Rules >= 0.5a1.dev-r2569",
        "repoze.what-pylons >= 1.0rc3",
        "WebError >= 0.10.1",
        "Pylons >= 0.9.7",
        "repoze.who >= 1.0.10",
        "sqlalchemy-migrate >= 0.5.1",
        "repoze.what.plugins.sql >= 1.0rc1",
        "repoze.who.plugins.sa >= 1.0rc1",
        "repoze.what >= 1.0.3",
        "Extremes >= 1.1",
        "AddOns >= 0.6",
        "DecoratorTools >= 1.7dev-r2450",
        "BytecodeAssembler >= 0.3",
        "Pygments",
        "Tempita",
        "WebTest >= 1.1",
        "Mako >= 0.2.4",
        "nose >= 0.10.4",
        "WebHelpers >= 0.6.4",
        "repoze.who-testutil>=1.0b2",
        "SymbolType >= 1.0",
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
    data_files=install_i18n("i18n", "/usr/share/locale") +
        [(os.path.join(sysconfdir, "vigilo/models"), ["deployment/settings.ini"])],
)

