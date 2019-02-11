#!/bin/bash
# lié à 039_HLS_refactoring
# Copyright (C) 2014-2019 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

export PATH=/sbin:/bin:/usr/sbin:/usr/bin

while read -r -d '' file; do
    dir=`dirname "$file"`
    # nouveau répertoire (pas d'écrasement de l'ancienne configuration) pour placer les fichiers corrigés
    dir_post=`printf "%s" "$dir" | sed -e "s#/etc/vigilo/vigiconf/conf.d#/etc/vigilo/vigiconf/conf.d.post.039_HLS_refactoring#g"`

    if [ "$dir" == "$dir_post" ] ; then
        echo "Problème avec le répertoire destination: $dir_post" >&2
        exit 1
    fi
    mkdir -p "$dir_post"
    file=`basename "$file"`
    # suppression de la ligne si elle comporte uniquement la balise weight sur l'host:
    #     ' <weight>42</weight>'
    # suppression de la balise weight sur l'host :
    #     '<weight>42</weight>'
    # suppression des arguments sur le service :
    #     ' weight="45"'
    #     ' warning_weight="43"'
    cat "$dir/$file" | sed  -e '/^[ \t]*<weight>[0-9]\+<\/weight>[ \t]*$/d' \
                            -e "s#<weight>[0-9]\+</weight>##g" \
                            -e '/^[ \t]*<default_service_weight>[0-9]\+<\/default_service_weight>[ \t]*$/d' \
                            -e "s#<default_service_weight>[0-9]\+</default_service_weight>##g" \
                            -e '/^[ \t]*<default_service_warning_weight>[0-9]\+<\/default_service_warning_weight>[ \t]*$/d' \
                            -e "s#<default_service_warning_weight>[0-9]\+</default_service_warning_weight>##g" \
                            -e "s#[ \t]\+weight=\"[0-9]\+\"##g" \
                            -e "s#[ \t]\+warning_weight=\"[0-9]\+\"##g" > "$dir_post/$file"
    # si le fichier produit est identique à l'original il est supprimé.
    cmp -s "$dir/$file" "$dir_post/$file" && rm "$dir_post/$file"
done < <(find /etc/vigilo/vigiconf/conf.d/hosts/ /etc/vigilo/vigiconf/conf.d/hosttemplates/ -type f -a -name "*.xml" -print0)
