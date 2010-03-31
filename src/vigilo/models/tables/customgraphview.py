# -*- coding: utf-8 -*-
"""Modèle pour la table CustomGraphView."""
from sqlalchemy import Column
from sqlalchemy.types import Unicode, Integer

from vigilo.models.session import DeclarativeBase, DBSession, ForeignKey
from vigilo.models.tables.user import User
from vigilo.models.tables.graph import Graph
from vigilo.models.tables.host import Host

__all__ = ('CustomGraphView', )

class CustomGraphView(DeclarativeBase, object):
    """
    Gère les vues personnalisées d'un utilisateur dans VigiGraph.
    Cette classe permet aux utilisateurs de VigiGraph de sauvegarder
    l'ensemble des graphes affichés à l'écran à un instant donné.
    Elle pourra aussi être utilisée pour enregistrer les graphes affichés
    lorsque l'utilisateur se déconnecte, afin de les réafficher automatiquement
    lorsqu'il se reconnecte.

    @ivar viewname: Nom de la vue personnalisée.
    @ivar username: Nom de l'utilisateur auquel se rapporte la vue.
    @ivar idgraph: Identifiant du graphe ouvert.
    @ivar hostname: Nom de l'hôte auquel se rapporte le graphe.
    @ivar x_pos: Abscisse du graphe à l'écran.
    @ivar y_pos: Ordonnée du graphe à l'écran.
    """

    __tablename__ = 'customgraphview'

    viewname = Column(
        Unicode(255),
        primary_key=True)

    username = Column(
        Unicode(255),
        ForeignKey(
            User.user_name,
            onupdate="CASCADE", ondelete="CASCADE"),
        index=True, nullable=False, primary_key=True)

    idgraph = Column(
        Integer,
        ForeignKey(
            Graph.idgraph,
            onupdate="CASCADE", ondelete="CASCADE"),
        index=True, nullable=False, primary_key=True, autoincrement=False)

    hostname = Column(
        Unicode(255),
        ForeignKey(
            Host.name,
            onupdate="CASCADE", ondelete="CASCADE"),
        index=True, nullable=False, primary_key=True)

    x_pos = Column(
        Integer,
        nullable=False)

    y_pos = Column(
        Integer,
        nullable=False)

    def __init__(self, **kwargs):
        """Initialise une vue."""   
        super(CustomGraphView, self).__init__(**kwargs)

    @classmethod
    def by_view_and_user(cls, viewname, username):
        return DBSession.query(cls
            ).filter(cls.viewname == viewname
            ).filter(cls.username == username
            ).first()

