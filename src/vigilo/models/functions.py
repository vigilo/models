# -*- coding: utf-8 -*-
# Copyright (C) 2011-2015 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Bibliothèque pour faciliter certaines opérations sur le modèle."""
__all__ = ('sql_escape_like', )

def sql_escape_like(s):
    """
    Renvoie une chaine de caractères compatible avec l'opérateur
    LIKE de SQL.
    
    @param s: Chaine de caractère d'origine.
    @type s: C{unicode}
    @note: La chaine de caratère L{s} peut contenir les caractères
    spéciaux '?' et '*' qui agissent comme jokers et correspondent
    aux jokers '_' et '%' de SQL.
    """
    return s.replace('%', '\\%').replace('_', '\\_') \
                .replace('*', '%').replace('?', '_')

