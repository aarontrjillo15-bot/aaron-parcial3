import unittest

from calculadora.modelo import MAX_EXPRESION, Calculadora, formatear, tecla_desde_teclado


def teclear(calc, secuencia):
    """Pulsa cada elemento de una lista de teclas (o cada caracter de un texto)."""
    for tecla in secuencia:
        calc.pulsar(tecla)
    return calc


class PruebasModelo(unittest.TestCase):
    def setUp(self):
        self.calc = Calculadora()

    def test_suma_con_prioridad_de_operadores(self):
        teclear(self.calc, ["2", "+", "3", "×", "4", "="])
        self.assertEqual(self.calc.pantalla, "14")

    def test_parentesis_y_potencia(self):
        teclear(self.calc, ["(", "1", "+", "2", ")", "^", "3", "="])
        self.assertEqual(self.calc.pantalla, "27")

    def test_division_y_decimales(self):
        teclear(self.calc, ["1", "÷", "4", "="])
        self.assertEqual(self.calc.pantalla, "0.25")

    def test_ruido_de_coma_flotante_se_redondea(self):
        teclear(self.calc, ["0", ".", "1", "+", "0", ".", "2", "="])
        self.assertEqual(self.calc.pantalla, "0.3")

    def test_modulo(self):
        teclear(self.calc, ["1", "7", "mod", "5", "="])
        self.assertEqual(self.calc.pantalla, "2")

    def test_division_entre_cero_muestra_mensaje(self):
        teclear(self.calc, ["1", "÷", "0", "="])
        self.assertTrue(self.calc.hay_error)
        self.assertIn("cero", self.calc.mensaje)
        self.assertEqual(self.calc.expresion, "1÷0")  # no se pierde lo escrito

    def test_error_desaparece_al_seguir_escribiendo(self):
        teclear(self.calc, ["1", "÷", "0", "=", "⌫", "5", "="])
        self.assertFalse(self.calc.hay_error)
        self.assertEqual(self.calc.pantalla, "0.2")

    def test_expresion_incompleta(self):
        teclear(self.calc, ["5", "+", "="])
        self.assertTrue(self.calc.hay_error)

    def test_cierra_parentesis_abiertos_al_evaluar(self):
        teclear(self.calc, ["(", "2", "+", "3", "="])
        self.assertEqual(self.calc.pantalla, "5")

    def test_no_permite_cerrar_sin_abrir(self):
        teclear(self.calc, ["5", ")"])
        self.assertEqual(self.calc.expresion, "5")

    def test_multiplicacion_implicita(self):
        teclear(self.calc, ["2", "(", "3", "+", "4", ")", "="])
        self.assertEqual(self.calc.pantalla, "14")

    def test_operador_se_reemplaza(self):
        teclear(self.calc, ["5", "+", "×", "2", "="])
        self.assertEqual(self.calc.pantalla, "10")

    def test_no_permite_ceros_a_la_izquierda(self):
        teclear(self.calc, ["0", "0", "7"])
        self.assertEqual(self.calc.expresion, "7")

    def test_un_solo_punto_por_numero(self):
        teclear(self.calc, ["1", ".", "5", ".", "2"])
        self.assertEqual(self.calc.expresion, "1.52")

    def test_punto_al_inicio_agrega_cero(self):
        teclear(self.calc, ["."])
        self.assertEqual(self.calc.expresion, "0.")

    def test_menos_unario_al_inicio(self):
        teclear(self.calc, ["−", "5", "+", "8", "="])
        self.assertEqual(self.calc.pantalla, "3")

    def test_cambiar_signo(self):
        teclear(self.calc, ["5", "±"])
        self.assertEqual(self.calc.expresion, "(−5)")
        teclear(self.calc, ["+", "8", "="])
        self.assertEqual(self.calc.pantalla, "3")
        teclear(self.calc, ["C", "5", "±", "±"])
        self.assertEqual(self.calc.expresion, "5")

    def test_resultado_negativo_se_puede_seguir_usando(self):
        teclear(self.calc, ["2", "−", "5", "=", "×", "2", "="])
        self.assertEqual(self.calc.pantalla, "−6")

    def test_digito_tras_resultado_empieza_de_nuevo(self):
        teclear(self.calc, ["2", "+", "2", "=", "9"])
        self.assertEqual(self.calc.expresion, "9")

    def test_operador_tras_resultado_continua(self):
        teclear(self.calc, ["2", "+", "2", "=", "×", "3", "="])
        self.assertEqual(self.calc.pantalla, "12")

    def test_borrar_y_limpiar(self):
        teclear(self.calc, ["1", "2", "mod", "⌫"])
        self.assertEqual(self.calc.expresion, "12")
        teclear(self.calc, ["C"])
        self.assertEqual(self.calc.pantalla, "0")

    def test_historial_guarda_operaciones(self):
        teclear(self.calc, ["2", "+", "3", "=", "C", "4", "×", "5", "="])
        self.assertEqual(self.calc.historial, [("2+3", "5"), ("4×5", "20")])
        self.calc.borrar_historial()
        self.assertEqual(self.calc.historial, [])

    def test_historial_tiene_limite(self):
        for _ in range(30):
            teclear(self.calc, ["1", "+", "1", "=", "C"])
        self.assertEqual(len(self.calc.historial), 20)

    def test_potencia_enorme_se_rechaza_sin_colgarse(self):
        teclear(self.calc, ["9", "^", "9", "^", "9", "="])
        self.assertTrue(self.calc.hay_error)

    def test_resultado_demasiado_grande(self):
        teclear(self.calc, ["9", "9", "9", "^", "9", "9", "9", "="])
        self.assertTrue(self.calc.hay_error)

    def test_limite_de_longitud(self):
        teclear(self.calc, ["1"] * (MAX_EXPRESION + 20))
        self.assertEqual(len(self.calc.expresion), MAX_EXPRESION)
        self.assertTrue(self.calc.hay_error)

    def test_enteros_largos_pasan_a_notacion_cientifica(self):
        self.assertEqual(formatear(2**100), "1.2676506e+30")
        self.assertEqual(formatear(14.0), "14")
        self.assertEqual(formatear(123456789), "123456789")

    def test_usar_resultado_del_historial(self):
        teclear(self.calc, ["2", "−", "5", "="])
        self.calc.usar_resultado("-3")
        self.assertEqual(self.calc.expresion, "−3")

    def test_teclado_fisico(self):
        self.assertEqual(tecla_desde_teclado("7"), "7")
        self.assertEqual(tecla_desde_teclado("*"), "×")
        self.assertEqual(tecla_desde_teclado("-"), "−")
        self.assertEqual(tecla_desde_teclado("/"), "÷")
        self.assertEqual(tecla_desde_teclado(",", ""), ".")
        self.assertEqual(tecla_desde_teclado("\x08", "BackSpace"), "⌫")
        self.assertEqual(tecla_desde_teclado("", "Escape"), "C")
        self.assertEqual(tecla_desde_teclado("\r", "Return"), "=")
        self.assertIsNone(tecla_desde_teclado("a"))
        self.assertIsNone(tecla_desde_teclado("_"))

    def test_nunca_ejecuta_codigo(self):
        # Por la interfaz solo entran teclas validas; aun asi, texto arbitrario no cambia nada.
        teclear(self.calc, 'import os; __import__("os")')
        self.assertEqual(self.calc.expresion, "(")  # letras y comillas se ignoran; "(" es valido
        teclear(self.calc, ["="])
        self.assertTrue(self.calc.hay_error)


if __name__ == "__main__":
    unittest.main()
