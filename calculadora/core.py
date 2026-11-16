"""Nucleo de la calculadora.

VERSION 1.1 - segura frente a inyeccion de codigo.
En lugar de eval(), la expresion se convierte en un arbol (ast) y solo se
permiten numeros y operadores aritmeticos. Cualquier otra cosa se rechaza.
"""

import ast
import operator

# Operadores permitidos (lista blanca).
_BINARIOS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARIOS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

MAX_LONGITUD = 200  # evita expresiones gigantes
MAX_EXPONENTE = 1000  # evita 9**9**9 y consumo excesivo de CPU/memoria


class ExpresionInvalida(ValueError):
    """La expresion contiene algo que no es una operacion aritmetica valida."""


def _evaluar(nodo):
    if isinstance(nodo, ast.Expression):
        return _evaluar(nodo.body)
    if isinstance(nodo, ast.Constant) and type(nodo.value) in (int, float):
        return nodo.value
    if isinstance(nodo, ast.UnaryOp) and type(nodo.op) in _UNARIOS:
        return _UNARIOS[type(nodo.op)](_evaluar(nodo.operand))
    if isinstance(nodo, ast.BinOp) and type(nodo.op) in _BINARIOS:
        izquierda = _evaluar(nodo.left)
        derecha = _evaluar(nodo.right)
        if isinstance(nodo.op, ast.Pow) and abs(derecha) > MAX_EXPONENTE:
            raise ExpresionInvalida("exponente demasiado grande")
        return _BINARIOS[type(nodo.op)](izquierda, derecha)
    raise ExpresionInvalida("operacion no permitida")


def calcular(expresion: str):
    """Evalua una expresion aritmetica de forma segura."""
    if not isinstance(expresion, str) or not expresion.strip():
        raise ExpresionInvalida("expresion vacia")
    if len(expresion) > MAX_LONGITUD:
        raise ExpresionInvalida("expresion demasiado larga")
    try:
        arbol = ast.parse(expresion.strip(), mode="eval")
    except SyntaxError as error:
        raise ExpresionInvalida("sintaxis invalida") from error
    return _evaluar(arbol)
