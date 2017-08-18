# -*- coding: utf-8 -*-
# Copyright (C) 2006-2016 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>
"""
Commandes utilisables avec l'outil de gestion
des permissions.
"""

from __future__ import print_function
import transaction
from sqlalchemy.sql.expression import func
from vigilo.common.gettext import translate
_ = translate(__name__)

from vigilo.models.session import DBSession
from vigilo.models import tables
from vigilo.common import parse_path
from vigilo.common.logging import get_logger
LOGGER = get_logger(__name__)

_permissions = {
    'ro': u'r',
    'rw': u'w',
}

_reverse_permissions = {
    # TRANSLATORS: Used in a sentence such as:
    # TRANSLATORS: "Added ... permission on Foo for usergroup Bar".
    u'r': _('read-only'),

    # TRANSLATORS: Used in a sentence such as:
    # TRANSLATORS: "Added ... permission on Foo for usergroup Bar".
    u'w': _('read/write'),

    # TRANSLATORS: Used in a sentence such as:
    # TRANSLATORS: "Removed ... permission on Foo for usergroup Bar".
    None: _('all'),
}

_objects = {
    'monitored': tables.SupItemGroup,
    'map': tables.MapGroup,
    'graph': tables.GraphGroup,
    'user': tables.UserGroup,
}


def cmd_add(options):
    """
    Change les permissions d'un groupe d'utilisateurs
    vis-à-vis d'un groupe d'objets.

    @param options: Options et arguments passés au script.
    @type options: C{argparse.Namespace}
    @return: Code de sortie (0 = pas d'erreur, autre = erreur).
    @rtype: C{int}
    """
    permission = _permissions[options.permission]
    object_type = _objects[options.object_type]

    # Vérifications sur le groupe d'utilisateurs.
    usergroup_name = options.usergroup.decode('utf-8')
    usergroup = tables.UserGroup.by_group_name(usergroup_name)
    if usergroup is None:
        print(_("No such usergroup '%s'") % usergroup_name)
        return 2

    # Vérification sur le chemin du/des groupe(s) d'objets.
    group_path = options.object_group.decode('utf-8')
    group_parts = parse_path(group_path)
    if group_parts is None:
        print(_("Could not parse <object group> (%s). "
                "Make sure the value is correct and try again.") % group_path)
        return 2

    if len(group_parts) == 1 and not group_path == '/':
        # Chemin relatif.
        object_groups = DBSession.query(object_type
            ).filter(object_type.name == group_parts[0]).all()
    else:
        # Chemin absolu.
        object_groups = [object_type.by_path(group_path)]

    if (not object_groups) or object_groups[0] is None:
        print(_("No match found for group '%(group)s' "
                "with type '%(type)s'.") % {
                    'group': group_path,
                    'type': options.object_type,
                })
        return 2

    object_groups.sort(key=lambda x: x.path.lower())
    if len(object_groups) > 1 and not options.batch:
        print(_("Multiple groups named '%(group)s' "
                "with type '%(type)s' were found. "
                "Use --batch to set permissions "
                "on multiple groups at once.") % {
                    'group': group_path,
                    'type': options.object_type,
                })
        print(_("The following groups were found:"))
        for group in object_groups:
            print("-", group.path.encode('utf-8'))
        return 2

    datapermissions = {}
    for dataperm in usergroup.datapermissions:
        datapermissions[dataperm.idgroup] = dataperm

    # Ajout/mise à jour des permissions.
    for group in object_groups:
        # Il existe déjà une permission pour ce groupe d'utilisateurs
        # et ce groupe d'objets.
        if group.idgroup in datapermissions:
            # Si les permissions sont déjà les bonnes, on ne fait rien.
            if datapermissions[group.idgroup].access == permission:
                LOGGER.info(_(
                    "Usergroup '%(usergroup)s' already has "
                    "%(perm)s permissions on '%(path)s'. "
                    "No change required.") % {
                        'usergroup': usergroup_name,
                        'perm': _reverse_permissions[permission],
                        'path': datapermissions[group.idgroup].group.path,
                    })
                continue

            # Sinon, si on est en mode ajout, il y a conflit.
            if not options.update:
                print(_("Conflict detected: usergroup '%(usergroup)s' "
                        "already has %(perm)s permissions on '%(path)s'.") \
                        % {
                            'usergroup': usergroup_name,
                            'perm': _reverse_permissions[permission],
                            'path': datapermissions[group.idgroup].group.path,
                        })
                return 2

            # Mode mise à jour. On s'exécute.
            datapermissions[group.idgroup].access = permission

        # Sinon, on ajoute la nouvelle permission,
        # et on ajoute l'objet créé dans le cache
        # pour la prochaine itération.
        else:
            datapermissions[group.idgroup] = tables.DataPermission(
                idusergroup=usergroup.idgroup,
                idgroup=group.idgroup,
                access=permission,
            )

        # Ajout de l'object créé ou mis à jour à la session,
        # afin de sauvegarde son état lors du prochain flush().
        DBSession.add(datapermissions[group.idgroup])
        LOGGER.info(_("Successfully set %(perm)s permissions on '%(path)s' "
                      "for usergroup '%(usergroup)s'.") % {
                        'usergroup': usergroup_name,
                        'perm': _reverse_permissions[permission],
                        'path': group.path,
                      })

    DBSession.flush()
    if options.commit:
        transaction.commit()

    print(_("Successfully set %(perm)s permissions on %(nb_groups)d "
            "groups for usergroup '%(usergroup)s'.") % {
                'perm': _reverse_permissions[permission],
                'usergroup': usergroup_name,
                'nb_groups': len(object_groups),
            })
    return 0


def cmd_remove(options):
    """
    Supprime les permissions d'un groupe d'utilisateurs
    vis-à-vis d'un groupe d'objets.

    @param options: Options et arguments passés au script.
    @type options: C{argparse.Namespace}
    @return: Code de sortie (0 = pas d'erreur, autre = erreur).
    @rtype: C{int}
    """
    if options.permission is None:
        permission = None
    else:
        permission = _permissions[options.permission]
    object_type = _objects[options.object_type]

    # Vérifications sur le groupe d'utilisateurs.
    usergroup_name = options.usergroup.decode('utf-8')
    usergroup = tables.UserGroup.by_group_name(usergroup_name)
    if usergroup is None:
        print(_("No such usergroup '%s'") % usergroup_name)
        return 2

    # Vérification sur le chemin du/des groupe(s) d'objets.
    group_path = options.object_group.decode('utf-8')
    group_parts = parse_path(group_path)
    if group_parts is None:
        print(_("Could not parse <object group> (%s). "
                "Make sure the value is correct and try again.") % group_path)
        return 2

    if len(group_parts) == 1 and not group_path == '/':
        # Chemin relatif.
        object_groups = DBSession.query(object_type
            ).join(
                (tables.DataPermission, \
                    tables.DataPermission.idgroup == object_type.idgroup),
            ).filter(tables.DataPermission.idusergroup == usergroup.idgroup
            ).filter(object_type.name == group_parts[0])

        # Si on a spécifié un type particulier de permission
        # à supprimer et que le type de la permission courante
        # est différent, on l'ignore.
        if permission:
            object_groups = object_groups.filter(
                tables.DataPermission.access == permission)
        object_groups = object_groups.all()
    else:
        # Chemin absolu.
        object_groups = [object_type.by_path(group_path)]

    object_groups.sort(key=lambda x: x.path.lower())
    if (not object_groups) or object_groups[0] is None:
        if permission:
            print(_("No match found for group '%(group)s' "
                    "with type '%(type)s'.") % {
                        'group': group_path,
                        'type': options.object_type,
                    })
            return 2
        else:
            print(_("No match found for group '%(group)s' "
                    "with type '%(type)s' and permission '%(perm)s'.") % {
                        'group': group_path,
                        'type': options.object_type,
                        'perm': options.permission,
                    })
            return 2

    if len(object_groups) > 1 and not options.batch:
        print(_("Multiple groups named '%(group)s' "
                "with type '%(type)s' were found. "
                "Use --batch to set permissions "
                "on multiple groups at once.") % {
                    'group': group_path,
                    'type': options.object_type,
                })
        print(_("The following groups were found:"))
        for group in object_groups:
            print("-", group.path.encode('utf-8'))
        return 2

    idgroups = [group.idgroup for group in object_groups]
    removed = 0
    for dataperm in usergroup.datapermissions:
        # Si le groupe sur lequel porte la permission
        # ne fait pas partie des groupes visés, on l'ignore.
        if dataperm.idgroup not in idgroups:
            continue

        # Prise en compte du type de permission indiqué.
        # Nécessaire pour cas où on a passé un chemin absolu au script.
        if permission and dataperm.access != permission:
            continue

        # Sinon, on procède à la suppression de la permission.
        DBSession.delete(dataperm)
        LOGGER.info(_("Successfully removed %(perm)s permissions on '%(path)s' "
                      "for usergroup '%(usergroup)s'.") % {
                        'usergroup': usergroup_name,
                        'perm': _reverse_permissions[permission],
                        'path': group.path,
                      })
        removed += 1

    DBSession.flush()
    if options.commit:
        transaction.commit()

    print(_("Successfully removed %(perm)s permissions on %(nb_groups)d "
            "groups for usergroup '%(usergroup)s'.") % {
                'perm': _reverse_permissions[permission],
                'usergroup': usergroup_name,
                'nb_groups': removed,
            })
    return 0


def cmd_list(options):
    """
    Liste les objets d'un groupe donné.

    @param options: Options et arguments passés au script.
    @type options: C{argparse.Namespace}
    @return: Code de sortie (0 = pas d'erreur, autre = erreur).
    @rtype: C{int}
    """
    object_type = _objects[options.object_type]

    if object_type == tables.UserGroup:
        objects = DBSession.query(object_type.group_name
            ).order_by(func.lower(object_type.group_name))
    else:
        # ATTENTION : Le filter() devrait être superflu, mais il ne l'est pas !
        objects = DBSession.query(tables.GroupPath.path
            ).join(
                (object_type, object_type.idgroup == tables.GroupPath.idgroup),
            ).filter(object_type.grouptype ==
                object_type.__mapper_args__['polymorphic_identity']
            ).order_by(func.lower(tables.GroupPath.path))

    objects = objects.all()

    print(_("%(count)d groups found with type '%(type)s':") % {
                'type': options.object_type,
                'count': len(objects),
            })
    for obj in objects:
        print("-", obj[0].encode('utf-8'))
    return 0


def cmd_allow(options):
    """
    Ajoute des permissions sur les applications.

    @param options: Options et arguments passés au script.
    @type options: C{argparse.Namespace}
    @return: Code de sortie (0 = pas d'erreur, autre = erreur).
    @rtype: C{int}
    """

    # Vérifications sur les groupes d'utilisateurs.
    usergroups = set()
    for usergroup_name in options.usergroup:
        usergroup_name = usergroup_name.decode('utf-8')
        usergroup = tables.UserGroup.by_group_name(usergroup_name)
        if usergroup is None:
            print(_("No such usergroup '%s'") % usergroup_name)
        else:
            usergroups.add(usergroup)
    if not usergroups:
        print(_('No usergroup selected.'))
        return 2
    usergroups = sorted(usergroups, key=lambda ug: ug.group_name)

    # Vérifications sur les permissions.
    permissions = set()
    for permission_name in options.permissions.split(','):
        permission_name = permission_name.strip().decode('utf-8')
        permission = tables.Permission.by_permission_name(permission_name)
        if permission is None:
            print(_("No such permission '%s'.") % permission_name)
        else:
            permissions.add(permission)
    if not permissions:
        print(_('No permission selected.'))
        return 2
    permissions = sorted(permissions, key=lambda p: p.permission_name)

    for usergroup in usergroups:
        print(_("Adding permissions for usergroup '%s'.") % usergroup.group_name)
        usergroup.permissions.extend(permissions)

    DBSession.flush()
    if options.commit:
        transaction.commit()
    return 0


def cmd_deny(options):
    """
    Retire des permissions sur les applications.

    @param options: Options et arguments passés au script.
    @type options: C{argparse.Namespace}
    @return: Code de sortie (0 = pas d'erreur, autre = erreur).
    @rtype: C{int}
    """

    # Vérifications sur les groupes d'utilisateurs.
    usergroups = set()
    for usergroup_name in options.usergroup:
        usergroup_name = usergroup_name.decode('utf-8')
        usergroup = tables.UserGroup.by_group_name(usergroup_name)
        if usergroup is None:
            print(_("No such usergroup '%s'") % usergroup_name)
        else:
            usergroups.add(usergroup)
    if not usergroups:
        print(_('No usergroup selected.'))
        return 2
    usergroups = sorted(usergroups, key=lambda ug: ug.group_name)

    # Vérifications sur les permissions.
    permissions = set()
    for permission_name in options.permissions.split(','):
        permission_name = permission_name.strip().decode('utf-8')
        permission = tables.Permission.by_permission_name(permission_name)
        if permission is None:
            print(_("No such permission '%s'.") % permission_name)
        else:
            permissions.add(permission)
    if not permissions:
        print(_('No permission selected.'))
        return 2
    permissions = sorted(permissions, key=lambda p: p.permission_name)

    for usergroup in usergroups:
        print(_("Removing permissions for usergroup '%s'.") %
                usergroup.group_name)
        for permission in permissions:
            try:
                usergroup.permissions.remove(permission)
            except ValueError:
                pass

    DBSession.flush()
    if options.commit:
        transaction.commit()
    return 0


def cmd_duplicate(options):
    """
    Duplique les permissions sur les applications et/ou les données
    d'un groupe d'utilisateurs à un autre.

    @param options: Options et arguments passés au script.
    @type options: C{argparse.Namespace}
    @return: Code de sortie (0 = pas d'erreur, autre = erreur).
    @rtype: C{int}
    """

    # Vérifications sur les groupes d'utilisateurs.
    usergroups = []
    if options.usergroup[0] == options.usergroup[1]:
        print(_('Usergroup must be different'))
        return 2
    for usergroup_name in options.usergroup:
        usergroup_name = usergroup_name.decode('utf-8')
        usergroup = tables.UserGroup.by_group_name(usergroup_name)
        if usergroup is None:
            print(_("No such usergroup '%s'") % usergroup_name)
        else:
            usergroups.append(usergroup)
    if len(usergroups) != 2:
        print(_('Error on selected usergroups'))
        return 2

    # Sélection des groupes d'utilisateurs.
    usergroup_src = usergroups[0]
    usergroup_dst = usergroups[1]

    # Duplication des permissions sur les données.
    if options.permission_type == "all" or options.permission_type == "data":
        print(_("Adding %s's datapermissions to usergroup '%s'.") %
                (usergroup_src.group_name, usergroup_dst.group_name))

        datapermissions = {}

        # Récupération des permissions sur données du groupe d'utilisateurs destinataire
        for dataperm_dst in usergroup_dst.datapermissions:
            datapermissions[dataperm_dst.idgroup] = dataperm_dst

        # Duplication des permissions du groupe d'utilisateurs source vers
        # le groupe de destination
        for dataperm_src in usergroup_src.datapermissions:
            if dataperm_src.idgroup in datapermissions and \
                dataperm_src.access != datapermissions[dataperm_src.idgroup].access:
                datapermissions[dataperm_src.idgroup].access = dataperm_src.access
            elif dataperm_src.idgroup not in datapermissions:
                datapermissions[dataperm_src.idgroup] = tables.DataPermission(
                    idusergroup=usergroup_dst.idgroup,
                    idgroup=dataperm_src.idgroup,
                    access=dataperm_src.access,
                )
            # Ajout de la nouvelle permission sur donnée
            DBSession.add(datapermissions[dataperm_src.idgroup])
            LOGGER.info(_("Successfully set %(dataperm)s permissions "
                          "for usergroup '%(usergroup)s'.") % {
                            'usergroup': usergroup_dst.group_name,
                            'dataperm': _reverse_permissions[dataperm_src.access],
                          })
        print(_("Datapermissions duplication completed."))

    # Duplication des permissions sur les applications.
    if options.permission_type == "all" or options.permission_type == "apps":
        print(_("Adding %s's permissions to usergroup '%s'.") %
                (usergroup_src.group_name, usergroup_dst.group_name))
        usergroup_dst.permissions.extend(usergroup_src.permissions)
        print(_("Permissions duplication completed."))

    DBSession.flush()
    if options.commit:
        transaction.commit()
    return 0
