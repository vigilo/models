# -*- coding: utf-8 -*-
# Copyright (C) 2011-2019 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Classes et fonctions utilitaires autour du modèle Vigilo."""

from babel.dates import format_datetime
from datetime import datetime
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import UnicodeText


class DateMixin(object):
    def get_date(self, element, locale):
        """
        Permet de convertir une variable de temps en chaîne de caractères.
        Le format utilisé pour représenter la valeur dépend de la locale
        de l'utilisateur.

        @param element: nom de l'élément à convertir de la classe elle même
        @type element: C{unicode}
        @param locale: Locale de l'utilisateur.
        @type locale: C{basestring}
        @return: La date demandée.
        @rtype: C{unicode}
        """
        date = getattr(self, element)
        return format_datetime(date, format='medium', locale=locale)

    def get_since_date(self, element, locale):
        """
        Permet d'obtenir le temps écoulé entre maintenant (datetime.now())
        et le temps contenu dans la variable de temps indiquée.
        Le format utilisé pour représenter la valeur dépend de la locale
        de l'utilisateur.

        @param element: nom de l'élément de la classe à utiliser pour le calcul.
        @type element: C{unicode}
        @param locale: Locale de l'utilisateur.
        @type locale: C{basestring}
        @return: Le temps écoulé depuis la date demandée, ex: "4d 8h 15'".
        @rtype: C{unicode}
        """
        date = datetime.now() - getattr(self, element)
        minutes = divmod(date.seconds, 60)[0]
        hours, minutes = divmod(minutes, 60)
        return "%dd %dh %d'" % (date.days , hours , minutes)


class group_concat(expression.FunctionElement):
    """
    Définit une nouvelle fonction d'agrégation 'group_concat' utilisable dans
    les requêtes SQLAlchemy. Cette fonction prend 2 paramètres en entrée :
    - le nom d'une colonne ;
    - un séparateur (optionnel, par défaut ",").
    Elle retourne alors la concaténation de toutes les valeurs prises par la
    colonne en question, séparées par le second paramètre.
    """
    type = UnicodeText()
    name = "group_concat"

@compiles(group_concat, 'mysql')
def _group_concat_mysql(element, compiler, **kw):
    """Implémentation de la fonction group_concat pour MySQL"""
    if len(element.clauses) == 2:
        separator = compiler.process(element.clauses.clauses[1])
    else:
        separator = u','

    return u'GROUP_CONCAT(%s SEPARATOR %s)' % (
        compiler.process(element.clauses.clauses[0]),
        separator,
    )

@compiles(group_concat, 'sqlite')
def _group_concat_sqlite(element, compiler, **kw):
    """Implémentation de la fonction group_concat pour SQLite"""
    if len(element.clauses) == 2:
        separator = compiler.process(element.clauses.clauses[1])
    else:
        separator = u','

    return u'GROUP_CONCAT(%s, %s)' % (
        compiler.process(element.clauses.clauses[0]),
        separator,
    )

@compiles(group_concat, 'postgresql')
def _group_concat_postgresql(element, compiler, **kw):
    """Implémentation de la fonction group_concat pour PostgreSQL"""
    if len(element.clauses) == 2:
        separator = compiler.process(element.clauses.clauses[1])
    else:
        separator = u','

    return u'ARRAY_TO_STRING(ARRAY_AGG(%s), %s)' % (
        compiler.process(element.clauses.clauses[0]),
        separator,
    )
