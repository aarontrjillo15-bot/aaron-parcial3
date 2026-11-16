"""Configuracion de la calculadora: la clave se lee del entorno, nunca del codigo."""

import os

API_KEY = os.environ.get("API_KEY", "")