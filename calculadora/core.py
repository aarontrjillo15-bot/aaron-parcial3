"""Nucleo de la calculadora.

VERSION 1.0 - INTENCIONALMENTE INSEGURA (solo para la demo academica).
Usa eval() sobre texto escrito por el usuario: CWE-95 (inyeccion de codigo).
CodeQL detecta este patron. La version 1.1 lo corrige.
"""


def calcular(expresion: str):
    """Evalua una expresion aritmetica escrita por el usuario."""
    return eval(expresion)
