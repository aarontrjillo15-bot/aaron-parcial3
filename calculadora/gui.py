"""Calculadora con ventana y botones (tkinter, ya incluido en Python).

Toda la logica vive en calculadora.modelo; este modulo solo dibuja la ventana y reenvia
las pulsaciones (botones o teclado) al modelo.
"""

from calculadora import __version__
from calculadora.modelo import Calculadora, tecla_desde_teclado

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:  # Linux sin el paquete python3-tk
    tk = None
    ttk = None

# Paleta (fondo oscuro, acento naranja en "=")
FONDO = "#1e1f26"
PANTALLA = "#14151a"
TEXTO = "#f2f3f7"
TEXTO_SUAVE = "#9aa0b4"
ERROR = "#ff7b72"
NUMERO = "#2e3040"
NUMERO_ACTIVO = "#3b3e52"
OPERADOR = "#3d4a7a"
OPERADOR_ACTIVO = "#4b5a94"
ACCION = "#5a3a45"
ACCION_ACTIVO = "#744a58"
IGUAL = "#e8833a"
IGUAL_ACTIVO = "#f09a5a"

# (texto, tecla, estilo, columnas que ocupa)
FILAS = (
    (("C", "C", "Accion", 1), ("⌫", "⌫", "Accion", 1), ("(", "(", "Operador", 1),
     (")", ")", "Operador", 1), ("÷", "÷", "Operador", 1)),
    (("7", "7", "Numero", 1), ("8", "8", "Numero", 1), ("9", "9", "Numero", 1),
     ("×", "×", "Operador", 1), ("xʸ", "^", "Operador", 1)),
    (("4", "4", "Numero", 1), ("5", "5", "Numero", 1), ("6", "6", "Numero", 1),
     ("−", "−", "Operador", 1), ("mod", "mod", "Operador", 1)),
    (("1", "1", "Numero", 1), ("2", "2", "Numero", 1), ("3", "3", "Numero", 1),
     ("+", "+", "Operador", 1), ("±", "±", "Operador", 1)),
    (("0", "0", "Numero", 2), (".", ".", "Numero", 1), ("=", "=", "Igual", 2)),
)


class VentanaCalculadora:
    def __init__(self, raiz):
        self.raiz = raiz
        self.calc = Calculadora()

        raiz.title("Calculadora segura  v" + __version__)
        raiz.configure(bg=FONDO)
        raiz.minsize(560, 470)

        self._estilos()
        self._construir()
        self._vincular_teclado()
        self.actualizar()

    # ---------------------------------------------------------------- estilos
    def _estilos(self):
        estilo = ttk.Style(self.raiz)
        try:
            estilo.theme_use("clam")  # el unico tema que respeta colores en todos los sistemas
        except tk.TclError:
            pass
        for nombre, fondo, activo, color in (
            ("Numero", NUMERO, NUMERO_ACTIVO, TEXTO),
            ("Operador", OPERADOR, OPERADOR_ACTIVO, TEXTO),
            ("Accion", ACCION, ACCION_ACTIVO, TEXTO),
            ("Igual", IGUAL, IGUAL_ACTIVO, "#1b1308"),
        ):
            estilo.configure(
                nombre + ".TButton", background=fondo, foreground=color,
                font=("Segoe UI", 16, "bold"), borderwidth=0, focusthickness=0,
                focuscolor=fondo, relief="flat", padding=(0, 10),
            )
            estilo.map(nombre + ".TButton", background=[("pressed", activo), ("active", activo)])
        estilo.configure(
            "Historial.TButton", background=NUMERO, foreground=TEXTO_SUAVE,
            font=("Segoe UI", 10), borderwidth=0, focusthickness=0, focuscolor=NUMERO,
            padding=(0, 6),
        )
        estilo.map("Historial.TButton", background=[("active", NUMERO_ACTIVO)])

    # ----------------------------------------------------------- construccion
    def _construir(self):
        marco = tk.Frame(self.raiz, bg=FONDO)
        marco.pack(fill="both", expand=True, padx=12, pady=12)
        marco.columnconfigure(0, weight=3)
        marco.columnconfigure(1, weight=2)
        marco.rowconfigure(0, weight=1)

        # ---- columna izquierda: pantalla + teclado
        izquierda = tk.Frame(marco, bg=FONDO)
        izquierda.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        izquierda.columnconfigure(0, weight=1)

        pantalla = tk.Frame(izquierda, bg=PANTALLA)
        pantalla.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        pantalla.columnconfigure(0, weight=1)
        self.linea_superior = tk.Label(
            pantalla, text="", bg=PANTALLA, fg=TEXTO_SUAVE, anchor="e",
            font=("Segoe UI", 11), padx=14, pady=10,
        )
        self.linea_superior.grid(row=0, column=0, sticky="ew")
        self.visor = tk.Label(
            pantalla, text="0", bg=PANTALLA, fg=TEXTO, anchor="e",
            font=("Segoe UI", 34, "bold"), padx=14, pady=0,
        )
        self.visor.grid(row=1, column=0, sticky="ew", pady=(0, 12))

        teclado = tk.Frame(izquierda, bg=FONDO)
        teclado.grid(row=1, column=0, sticky="nsew")
        izquierda.rowconfigure(1, weight=1)
        for columna in range(5):
            teclado.columnconfigure(columna, weight=1, uniform="teclas")
        for fila, teclas in enumerate(FILAS):
            teclado.rowconfigure(fila, weight=1)
            columna = 0
            for texto, tecla, estilo, ancho in teclas:
                boton = ttk.Button(
                    teclado, text=texto, style=estilo + ".TButton", takefocus=False,
                    command=lambda t=tecla: self.pulsar(t),
                )
                boton.grid(row=fila, column=columna, columnspan=ancho, sticky="nsew",
                           padx=3, pady=3)
                columna += ancho

        # ---- columna derecha: historial
        derecha = tk.Frame(marco, bg=FONDO)
        derecha.grid(row=0, column=1, sticky="nsew")
        derecha.rowconfigure(1, weight=1)
        derecha.columnconfigure(0, weight=1)
        tk.Label(derecha, text="Historial", bg=FONDO, fg=TEXTO_SUAVE, anchor="w",
                 font=("Segoe UI", 11, "bold")).grid(row=0, column=0, columnspan=2, sticky="ew")
        self.lista = tk.Listbox(
            derecha, bg=PANTALLA, fg=TEXTO, selectbackground=OPERADOR, selectforeground=TEXTO,
            font=("Consolas", 12), borderwidth=0, highlightthickness=0, activestyle="none",
            exportselection=False,
        )
        self.lista.grid(row=1, column=0, sticky="nsew", pady=(6, 6))
        barra = ttk.Scrollbar(derecha, orient="vertical", command=self.lista.yview)
        barra.grid(row=1, column=1, sticky="ns", pady=(6, 6))
        self.lista.configure(yscrollcommand=barra.set)
        self.lista.bind("<Double-Button-1>", self._reusar_historial)
        ttk.Button(derecha, text="Borrar historial", style="Historial.TButton",
                   takefocus=False, command=self.borrar_historial).grid(
            row=2, column=0, columnspan=2, sticky="ew")
        tk.Label(derecha, text="Doble clic en una línea para reutilizar el resultado",
                 bg=FONDO, fg=TEXTO_SUAVE, font=("Segoe UI", 9), wraplength=200,
                 justify="left", anchor="w").grid(row=3, column=0, columnspan=2,
                                                  sticky="ew", pady=(8, 0))

    def _vincular_teclado(self):
        self.raiz.bind("<Key>", self._tecla_fisica)

    # ---------------------------------------------------------------- eventos
    def _tecla_fisica(self, evento):
        tecla = tecla_desde_teclado(evento.char, evento.keysym)
        if tecla is not None:
            self.pulsar(tecla)

    def pulsar(self, tecla):
        self.calc.pulsar(tecla)
        self.actualizar()

    def borrar_historial(self):
        self.calc.borrar_historial()
        self.actualizar()

    def _reusar_historial(self, _evento):
        seleccion = self.lista.curselection()
        if not seleccion:
            return
        _expresion, resultado = self.calc.historial[::-1][seleccion[0]]
        self.calc.usar_resultado(resultado)
        self.actualizar()

    # --------------------------------------------------------------- pantalla
    def actualizar(self):
        texto = self.calc.pantalla
        tamano = 34 if len(texto) <= 11 else 26 if len(texto) <= 16 else 20 if len(texto) <= 24 else 15
        self.visor.configure(text=texto, font=("Segoe UI", tamano, "bold"))
        self.linea_superior.configure(
            text=self.calc.linea_superior, fg=ERROR if self.calc.hay_error else TEXTO_SUAVE)
        self.lista.delete(0, "end")
        for expresion, resultado in reversed(self.calc.historial):  # la mas reciente arriba
            self.lista.insert("end", f"{expresion} = {resultado}")


def main():
    if tk is None:
        raise SystemExit(
            "Este Python no incluye tkinter.\n"
            "  Windows/macOS: reinstala Python desde python.org (marca 'tcl/tk').\n"
            "  Linux (Debian/Ubuntu): sudo apt install python3-tk"
        )
    raiz = tk.Tk()
    VentanaCalculadora(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()
