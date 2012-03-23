Configuration de la base de données
-----------------------------------
Pour fonctionner, le composant a besoin d'un accès à la base de données Vigilo.
Ce chapitre liste les options de configuration s'y rapportant.

Configuration basique
^^^^^^^^^^^^^^^^^^^^^
La configuration de la connexion à cette base de base de données se fait en
modifiant la valeur de la clé « sqlalchemy_url » sous la section [database].

Cette clé consiste en une URL (Uniform Resource Locator) qui définit tous les
paramètres nécessaires pour pouvoir se connecter à la base de données. Le
format de cette URL est le suivant::

    sgbd://nom_utilisateur:mot_de_passe@adresse_serveur:port_serveur/nom_base_de_donnees

Le champ « :port_serveur » est optionnel et peut être omis si vous utilisez le
port par défaut d'installation du SGBD choisi.

Par exemple, voici la valeur correspondant à une installation mono-poste par défaut::

    postgres://vigilo:vigilo@localhost/vigilo

..  warning::
    À l'heure actuelle, seul PostgreSQL a fait l'objet de tests intensifs.
    D'autres SGBD peuvent également fonctionner, mais aucun support ne sera
    fourni pour ces SGBD.

Choix d'un préfixe pour les tables de la base de données
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Il est recommandé de ne pas utiliser de préfixe pour les noms des tables mais
de privilégier l'installation de Vigilo dans une base de données séparée.
Néanmoins, vous pouvez choisir un préfixe qui sera appliqué aux noms des tables
de la base de données en indiquant ce préfixe dans la clé « db_basename » sous
la section [database].

Utilisez de préférence un préfixe ne contenant que des caractères
alpha-numériques ou le caractère « _ ».
