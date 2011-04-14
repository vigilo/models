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
- paste-script >= 1.7
- transaction


Installation
------------
L'installation se fait par la commande ``make install`` (à exécuter en
``root``).


License
-------
Models est sous licence `GPL v2`_.


.. _documentation officielle: Vigilo_
.. _Vigilo: http://www.projet-vigilo.org
.. _PostgreSQL: http://www.postgresql.org
.. _SQLAlchemy: http://www.sqlalchemy.org
.. _GPL v2: http://www.gnu.org/licenses/gpl-2.0.html

.. vim: set syntax=rst fileencoding=utf-8 tw=78 :


