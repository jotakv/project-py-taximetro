
# Pruebas automatizadas de US-07

import json
import tempfile
import unittest

from pathlib import Path
from unittest.mock import patch

import tarifas
from taxi import Taxi


class PruebasTarifas(unittest.TestCase):

    # Comprobar que podemos leer tarifas correctas
    def test_leer_tarifas(self):

        # Creamos una carpeta temporal para la prueba
        with tempfile.TemporaryDirectory() as carpeta:

            ruta = Path(carpeta) / "tarifas.json"

            # Escribimos un archivo de prueba
            datos = {
                "tarifa_parado": 0.02,
                "tarifa_movimiento": 0.05
            }

            ruta.write_text(
                json.dumps(datos), encoding="utf-8"
            )

            # Utilizamos el archivo temporal
            with patch.object(
                tarifas, "RUTA_CONFIGURACION", ruta
            ):

                parado, movimiento = tarifas.cargar_tarifas()

                self.assertEqual(parado, 0.02)
                self.assertEqual(movimiento, 0.05)

    # Comprobar que se rechazan tarifas negativas
    def test_rechazar_tarifa_negativa(self):

        with tempfile.TemporaryDirectory() as carpeta:

            ruta = Path(carpeta) / "tarifas.json"

            datos = {
                "tarifa_parado": -0.02,
                "tarifa_movimiento": 0.05
            }

            ruta.write_text(
                json.dumps(datos), encoding="utf-8"
            )

            with patch.object(
                tarifas, "RUTA_CONFIGURACION", ruta
            ):

                # Esperamos que se produzca ValueError
                with self.assertRaises(ValueError):
                    tarifas.cargar_tarifas()

    # Comprobar las dos tarifas en el cálculo
    def test_calcular_importe(self):

        taxi = Taxi()

        # Preparamos una carrera simulada
        taxi.carrera_activa = True
        taxi.ultimo_tiempo = 100.0

        taxi.tarifa_parado = 0.02
        taxi.tarifa_movimiento = 0.05

        # Simulamos 10 segundos con el taxi parado
        with patch(
            "taxi.time.monotonic",
            return_value=110.0
        ):
            taxi.calcular_importe()

        self.assertAlmostEqual(
            taxi.importe_total, 0.20
        )

        # Simulamos 10 segundos en movimiento
        taxi.en_movimiento = True

        with patch(
            "taxi.time.monotonic",
            return_value=120.0
        ):
            taxi.calcular_importe()

        # 0.20 + 0.50 = 0.70 euros
        self.assertAlmostEqual(
            taxi.importe_total, 0.70
        )

    # Comprobar que los cambios se aplican a otra carrera
    def test_recargar_tarifas_en_nueva_carrera(self):

        with tempfile.TemporaryDirectory() as carpeta:

            ruta = Path(carpeta) / "tarifas.json"

            ruta.write_text(
                json.dumps({
                    "tarifa_parado": 0.02,
                    "tarifa_movimiento": 0.05
                }),
                encoding="utf-8"
            )

            with patch.object(
                tarifas, "RUTA_CONFIGURACION", ruta
            ):

                taxi = Taxi()
                taxi.iniciar_carrera()

                self.assertEqual(taxi.tarifa_parado, 0.02)

                # Modificamos el archivo durante la carrera
                ruta.write_text(
                    json.dumps({
                        "tarifa_parado": 0.04,
                        "tarifa_movimiento": 0.10
                    }),
                    encoding="utf-8"
                )

                # La carrera actual conserva la tarifa
                self.assertEqual(taxi.tarifa_parado, 0.02)

                # Simulamos que la primera carrera terminó
                taxi.carrera_activa = False

                # Iniciamos la siguiente carrera
                taxi.iniciar_carrera()

                # Se aplican los nuevos precios
                self.assertEqual(taxi.tarifa_parado, 0.04)
                self.assertEqual(taxi.tarifa_movimiento, 0.10)


if __name__ == "__main__":
    unittest.main()
