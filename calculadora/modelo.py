"""Logica de la calculadora visual.

Este modulo NO usa tkinter: recibe pulsaciones de teclas y mantiene la expresion, el
historial y los mensajes de error. Asi se puede probar automaticamente sin abrir ventanas.
El calculo en si lo hace calculadora.core.calcular (evaluador seguro, sin eval).
"""

import re

from calculadora.core import ExpresionInvalida, calcular

DIGITOS = frozenset("0123456789")
OPERADORES = ("+", "−", "×", "÷", "^", " mod ")
MAX_HISTORIAL = 20
MAX_EXPRESION = 120  # menos que el limite del nucleo, porque "^" se convierte en "**"

# De lo que se ve en pantalla a lo que entiende el nucleo.
_TRADUCCION = (("×", "*"), ("÷", "/"), ("−", "-"), ("^", "**"), (" mod ", "%"))

# Teclas fisicas del teclado -> teclas de la calculadora.
_TECLADO = {
    "+": "+", "-": "−", "*": "×", "x": "×", "X": "×", "/": "÷", "^": "^",
    "%": "mod", "(": "(", ")": ")", ".": ".", ",": ".", "=": "=", "\r": "=",
}


def tecla_desde_teclado(caracter: str, keysym: str = ""):
    """Convierte una tecla fisica en una tecla de la calculadora (o None si no aplica)."""
    if keysym == "BackSpace":
        return "⌫"
    if keysym in ("Escape", "Delete"):
        return "C"
    if keysym in ("Return", "KP_Enter"):
        return "="
    if caracter in DIGITOS:
        return caracter
    return _TECLADO.get(caracter)


def formatear(valor) -> str:
    """Da formato legible a un resultado (14.0 -> '14', 0.30000000000000004 -> '0.3')."""
    if isinstance(valor, complex):
        raise ValueError("resultado no real")
    if isinstance(valor, bool):
        valor = int(valor)
    if isinstance(valor, float):
        if valor != valor or valor in (float("inf"), float("-inf")):
            raise OverflowError("resultado fuera de rango")
        return format(valor, ".12g")
    if isinstance(valor, int) and len(str(abs(valor))) > 16:
        return format(float(valor), ".10g")  # puede lanzar OverflowError si es enorme
    return str(valor)


class Calculadora:
    """Estado de la calculadora: expresion en pantalla, mensaje de error e historial."""

    def __init__(self):
        self.expresion = ""
        self.mensaje = ""
        self.historial = []  # lista de (expresion, resultado), la mas reciente al final
        self._mostrando_resultado = False

    # ------------------------------------------------------------------ pantalla
    @property
    def pantalla(self) -> str:
        return self.expresion if self.expresion else "0"

    @property
    def hay_error(self) -> bool:
        return bool(self.mensaje)

    @property
    def linea_superior(self) -> str:
        if self.mensaje:
            return self.mensaje
        if self._mostrando_resultado and self.historial:
            return self.historial[-1][0] + " ="
        return ""

    # ---------------------------------------------------------------- entrada
    def pulsar(self, tecla: str) -> None:
        """Procesa una tecla: digitos, operadores, '(' ')' '.' '±' '⌫' 'C' '='."""
        self.mensaje = ""
        if tecla == "C":
            self.expresion = ""
            self._mostrando_resultado = False
        elif tecla == "⌫":
            self._borrar()
        elif tecla == "=":
            self._evaluar()
        elif tecla == "±":
            self._cambiar_signo()
        elif tecla in DIGITOS:
            self._digito(tecla)
        elif tecla == ".":
            self._punto()
        elif tecla == "mod":
            self._operador(" mod ")
        elif tecla in ("+", "−", "×", "÷", "^"):
            self._operador(tecla)
        elif tecla == "(":
            self._abrir()
        elif tecla == ")":
            self._cerrar()

    def usar_resultado(self, texto: str) -> None:
        """Pone un resultado del historial en pantalla."""
        self.mensaje = ""
        self.expresion = texto.replace("-", "−")
        self._mostrando_resultado = True

    def borrar_historial(self) -> None:
        self.historial.clear()

    # ------------------------------------------------------------ utilidades
    def _lleno(self) -> bool:
        if len(self.expresion) >= MAX_EXPRESION:
            self.mensaje = "Expresión demasiado larga"
            return True
        return False

    def _empezar_nuevo(self) -> None:
        if self._mostrando_resultado:
            self.expresion = ""
            self._mostrando_resultado = False

    @staticmethod
    def _sin_operador_final(texto: str) -> str:
        for operador in OPERADORES:
            if texto.endswith(operador):
                return texto[: -len(operador)]
        return texto

    # ------------------------------------------------------------ teclas
    def _digito(self, digito: str) -> None:
        if self._lleno():
            return
        self._empezar_nuevo()
        if self.expresion.endswith(")"):
            self.expresion += "×"
        if re.search(r"(?<![\d.])0$", self.expresion):  # evita "007" (no es valido)
            if digito == "0":
                return
            self.expresion = self.expresion[:-1]
        self.expresion += digito

    def _punto(self) -> None:
        if self._lleno():
            return
        self._empezar_nuevo()
        if self.expresion.endswith(")"):
            self.expresion += "×"
        numero = re.search(r"[\d.]*$", self.expresion).group()
        if "." in numero:
            return
        if numero == "":
            self.expresion += "0"
        self.expresion += "."

    def _operador(self, operador: str) -> None:
        if self._lleno():
            return
        self._mostrando_resultado = False  # se sigue operando con el resultado
        expresion = self.expresion
        if expresion == "" or expresion.endswith("("):
            if operador == "−":  # solo se permite un signo menos al inicio
                self.expresion += operador
            return
        base = self._sin_operador_final(expresion)
        if base == "" or base.endswith("("):
            return
        self.expresion = base + operador

    def _abrir(self) -> None:
        if self._lleno():
            return
        self._empezar_nuevo()
        if self.expresion and (self.expresion[-1] in DIGITOS or self.expresion[-1] == ")"):
            self.expresion += "×"  # 2(3+4) se entiende como 2×(3+4)
        self.expresion += "("

    def _cerrar(self) -> None:
        if self._lleno():
            return
        abiertos = self.expresion.count("(") - self.expresion.count(")")
        if abiertos > 0 and self.expresion and (
            self.expresion[-1] in DIGITOS or self.expresion[-1] == ")"
        ):
            self.expresion += ")"

    def _borrar(self) -> None:
        self._mostrando_resultado = False
        if self.expresion.endswith(" mod "):
            self.expresion = self.expresion[:-5]
        else:
            self.expresion = self.expresion[:-1]

    def _cambiar_signo(self) -> None:
        self._mostrando_resultado = False
        negado = re.search(r"\(−(\d+\.?\d*)\)$", self.expresion)
        if negado:
            self.expresion = self.expresion[: negado.start()] + negado.group(1)
            return
        numero = re.search(r"(\d+\.?\d*)$", self.expresion)
        if numero:
            self.expresion = self.expresion[: numero.start()] + "(−" + numero.group(1) + ")"

    def _evaluar(self) -> None:
        expresion = self.expresion
        if not expresion or self._mostrando_resultado:
            return
        if expresion.endswith("(") or self._sin_operador_final(expresion) != expresion:
            self.mensaje = "Expresión incompleta"
            return
        completa = expresion + ")" * (expresion.count("(") - expresion.count(")"))
        codigo = completa
        for origen, destino in _TRADUCCION:
            codigo = codigo.replace(origen, destino)
        try:
            texto = formatear(calcular(codigo))
        except ExpresionInvalida:
            self.mensaje = "Expresión no válida"
            return
        except ZeroDivisionError:
            self.mensaje = "No se puede dividir entre cero"
            return
        except OverflowError:
            self.mensaje = "Resultado demasiado grande"
            return
        except ValueError:
            self.mensaje = "Resultado no válido"
            return
        self.historial.append((completa, texto))
        del self.historial[:-MAX_HISTORIAL]
        self.expresion = texto.replace("-", "−")
        self._mostrando_resultado = True
