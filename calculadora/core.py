"""Nucleo de la calculadora (rama de demo: reintroduce eval para que CodeQL lo detecte)."""


def calcular(expresion: str):
    """Evalua una expresion aritmetica escrita por el usuario."""
    return eval(expresion)
