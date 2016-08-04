Models
======

Ce module contient les classes ORM utilisées dans le cadre de Vigilo_. Il est
basé sur la bibliothèque SQLAlchemy_ et a été testé avec une base de données
PostgreSQL_, mais devrait pouvoir fonctionner avec un autre moteur de bases de
données.

Pour les détails du fonctionnement des modèles Vigilo, se reporter à la
`documentation officielle`_.


Dépendances
-----------
Vigilo nécessite une version de Python supérieure ou égale à 2.5. Le chemin de
l'exécutable python peut être passé en paramètre du ``make install`` de la
façon suivante::

    make install PYTHON=/usr/bin/python2.6

Les modèles ont besoin des modules Python suivants :

- setuptools (ou distribute)
- vigilo-common
- psycopg2 (pour PostgreSQL)
- sqlalchemy 0.5.x
- zope-sqlalchemy >= 0.4
- paste-deploy
- transaction


Installation
------------
L'installation se fait par la commande ``make install`` (à exécuter en
``root``).

Vous devez ensuite créer l'utilisateur et la base de données Vigilo. Exemple
sous PostgreSQL::

    sudo -u postgres createuser --no-inherit --no-createdb --no-createrole \
                                --no-superuser --pwprompt vigilo
    sudo -u postgres createdb vigilo --owner vigilo --encoding UTF8

Puis, dans le cas de PostgreSQL, il faut autoriser l'accès local à
l'utilisateur Vigilo dans la configuration du serveur. Pour cela, éditer le
fichier ``/var/lib/pgsql/data/pg_hba.conf`` et ajouter les lignes suivantes en
début de fichier::

    local   vigilo      vigilo                            md5
    host    vigilo      vigilo      127.0.0.1/32          md5
    host    vigilo      vigilo      ::1/128               md5

Et recharger le serveur PostgreSQL. Enfin, après avoir installé tous les
composants de Vigilo, vous pourrez initialiser la base de données Vigilo grâce
à la commande::

    vigilo-updatedb


License
-------
Models est sous licence `GPL v2`_.


.. _documentation officielle: Vigilo_
.. _Vigilo: http://www.projet-vigilo.org
.. _PostgreSQL: http://www.postgresql.org
.. _SQLAlchemy: http://www.sqlalchemy.org
.. _GPL v2: http://www.gnu.org/licenses/gpl-2.0.html

.. vim: set syntax=rst fileencoding=utf-8 tw=78 :
