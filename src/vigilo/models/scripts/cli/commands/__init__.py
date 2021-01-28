# -*- coding: utf-8 -*-
# Copyright (C) 2018-2021 CS GROUP - France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

# pylint: disable-msg=E1103
# E1103: Instance of 'False' has no 'error' member (but some types
#        could not be inferred)

from vigilo.common import parse_path
from vigilo.models.session import DBSession
from vigilo.models import tables
from vigilo.models.scripts.cli.main import PrerequisitesError

from vigilo.common.gettext import translate
_ = translate(__name__)

__all__ = ('CommandBase', )


class CommandBase(object):
    # Indique si un COMMIT doit avoir lieu dans la base de données
    # après l'opération ou non. Si l'opération se contente d'afficher
    # des données (lecture seule), passer l'attribut à False.
    commit = True

    # Message servant à décrire la commande (vigilo-cli --help).
    help = None

    def __init__(self, parser):
        """
        Configure le parser propre à la commande.
        Permet de déclarer les options/arguments attendus par la commande.

        @param parser: Le parser associé à la commande.
        """

    def execute(self, options, logger):
        """
        Exécute l'opération correspondant à la commande.

        @param options: Options et arguments passés à la commande,
            sous la forme d'un espace de noms C{argparse}.
        @type options: C{Namespace}
        @param logger: Logger pour la journalisation.
        @type logger: C{Logger}
        """

    # Méthodes outils qui reviennent fréquemment

    @staticmethod
    def _find_user(user, logger=False):
        """
        Retourne un utilisateur en fonction de son nom.

        Lève une exception si jamais l'utilisateur est introuvable.

        @param group: Nom de l'utilisateur.
        @type  group: C{str}
        @param logger: Logger vers lequel envoyer une trace
            si l'objet réclamé est introuvable.
        @type  logger: C{Logger}
        @return: L'objet représentant l'utilisateur.
        """
        user = user.decode('utf-8')
        obj = tables.User.by_user_name(user)
        if not obj:
            logger and logger.error(_('No such user "%s"'), user)
            raise PrerequisitesError(user)
        return obj

    @staticmethod
    def _find_usergroup(group, logger=False):
        """
        Retourne un groupe d'utilisateurs en fonction de son nom.

        Lève une exception si jamais le groupe est introuvable.

        @param group: Nom du groupe.
        @type  group: C{str}
        @param logger: Logger vers lequel envoyer une trace
            si l'objet réclamé est introuvable.
        @type  logger: C{Logger}
        @return: L'objet représentant le groupe.
        """
        group = group.decode('utf-8')
        obj = tables.UserGroup.by_group_name(group)
        if not obj:
            logger and logger.error(_('No such usergroup "%s"'), group)
            raise PrerequisitesError(group)
        return obj

    @staticmethod
    def _find_objgroup(objtype, path, logger=False):
        """
        Retourne un groupe d'objets en fonction de son chemin.

        Lève une exception si jamais le groupe est introuvable.

        @param objtype: Le type de groupe à rechercher.
        @param path: Chemin du groupe.
        @type  path: C{str}
        @param logger: Logger vers lequel envoyer une trace
            si l'objet réclamé est introuvable.
        @type  logger: C{Logger}
        @return: L'objet représentant le groupe d'objets.
        """
        # Vérification du format.
        path = path.decode('utf-8')
        group_parts = parse_path(path)
        if group_parts is None:
            logger and logger.error(_('Could not parse "%s"'), path)
            raise PrerequisitesError(path)

        # Validation du groupe.
        group = objtype.by_path(path)
        if not group:
            logger and logger.warning(_("No match found for group '%(group)s' "
                    "with type '%(type)s'."), {
                        'group': path,
                        'type': objtype,
                    })
            raise PrerequisitesError(path)

        return group
