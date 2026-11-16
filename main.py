"""Punto de entrada: calculadora interactiva de consola."""

from calculadora.core import ExpresionInvalida, calcular


def main() -> None:
    print("Calculadora (escribe 'salir' para terminar)")
    while True:
        try:
            texto = input("> ").strip()
        except EOFError:
            break
        if texto.lower() in {"salir", "exit", "q"}:
            break
        if not texto:
            continue
        try:
            print(calcular(texto))
        except ExpresionInvalida as error:
            print(f"Expresion no valida: {error}")
        except ZeroDivisionError:
            print("Error: division entre cero")
        except OverflowError:
            print("Error: resultado demasiado grande")


if __name__ == "__main__":
    main()
