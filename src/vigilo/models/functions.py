# -*- coding: utf-8 -*-
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
    au jokers '_' et '%' de SQL.
    """
    return s.replace('%', '\\%').replace('_', '\\_') \
                .replace('*', '%').replace('?', '_')

