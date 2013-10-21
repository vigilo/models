# -*- coding: utf-8 -*-
# Copyright (C) 2011-2013 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Classes et fonctions utilitaires autour du modèle Vigilo."""

from babel.dates import format_datetime
from datetime import datetime


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
