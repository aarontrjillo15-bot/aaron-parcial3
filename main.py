"""Punto de entrada: calculadora interactiva de consola."""

from calculadora.core import calcular


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
        except Exception as error:  # v1.0: captura todo, sin distinguir causas
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
