import unittest

from calculadora.core import ExpresionInvalida, calcular


class PruebasCalculadora(unittest.TestCase):
    def test_suma_y_precedencia(self):
        self.assertEqual(calcular("2+3*4"), 14)

    def test_parentesis_y_potencia(self):
        self.assertEqual(calcular("(1+2)**3"), 27)

    def test_decimales_y_negativos(self):
        self.assertAlmostEqual(calcular("-1.5 + 4"), 2.5)

    def test_division_entre_cero(self):
        with self.assertRaises(ZeroDivisionError):
            calcular("1/0")

    def test_rechaza_inyeccion_de_codigo(self):
        for ataque in (
            '__import__("os").system("echo hola")',
            "open('/etc/passwd').read()",
            "[x for x in range(3)]",
            "(lambda: 1)()",
        ):
            with self.subTest(ataque=ataque):
                with self.assertRaises(ExpresionInvalida):
                    calcular(ataque)

    def test_rechaza_exponente_enorme(self):
        with self.assertRaises(ExpresionInvalida):
            calcular("9**9**9")

    def test_rechaza_vacio_y_sintaxis_invalida(self):
        for texto in ("", "   ", "2 +", "2 $ 3"):
            with self.subTest(texto=texto):
                with self.assertRaises(ExpresionInvalida):
                    calcular(texto)

    def test_rechaza_expresion_larga(self):
        with self.assertRaises(ExpresionInvalida):
            calcular("1+" * 150 + "1")


if __name__ == "__main__":
    unittest.main()
