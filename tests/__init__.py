# -*- coding: utf-8 -*-
"""Unit test suite for the models of the application."""

from controller import setup_db, teardown_db

def setup():
    """Fonction appelée par nose au début des tests."""
    setup_db()

def teardown():
    """Fonction appelée par nose à la fin des tests."""
    teardown_db()

