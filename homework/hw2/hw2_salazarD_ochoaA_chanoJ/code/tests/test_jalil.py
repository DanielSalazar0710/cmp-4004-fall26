"""Pruebas de aceptación de la parte de Jalil. Al inicio fallan (las funciones
tienen NotImplementedError); al entregar deben pasar TODAS, sin Ollama.

    python code/tests/test_jalil.py
"""
import json
import math
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AQUI))

from llm_cliente import ClienteFalso  # noqa: E402
from problemas import ejemplos  # noqa: E402
from resultados import COLUMNAS, ERRORES_C, RAIZ, leer  # noqa: E402

PY = sys.executable


def test_prompt_sin_fugas():
    import respuesta_c
    for p in ejemplos():
        prompt = respuesta_c.construir_prompt(p)
        assert p["enunciado"] in prompt
        for v in p["formato_respuesta"]["variables"]:
            assert v in prompt
        assert "modelo_mano" not in prompt and "gold" not in prompt.lower()
        assert json.dumps(p["gold"]) not in prompt


def test_lector():
    import respuesta_c
    p = ejemplos()[0]
    gold = p["gold"]
    assert respuesta_c.leer_respuesta("Sure! ```json\n" + json.dumps(gold) + "\n```", p) == (gold, "")
    assert respuesta_c.leer_respuesta("I think Ana is in 3.", p)[1] == "sin_formato"
    assert respuesta_c.leer_respuesta('{"Ana": 3}', p)[1] == "incompleta"
    fuera = dict(gold, Ana=9)
    assert respuesta_c.leer_respuesta(json.dumps(fuera), p)[1] == "incompleta"


def test_fila_brazo_c():
    import brazo_c
    p = ejemplos()[0]
    fila = brazo_c.correr_problema(p, ClienteFalso(json.dumps(p["gold"])), 0, 0)
    assert set(fila) == set(COLUMNAS)
    assert fila["brazo"] == "C" and fila["resultado"] == "correcto" and fila["categoria_error"] == ""
    fila = brazo_c.correr_problema(p, ClienteFalso("no idea"), 1, 1)
    assert fila["resultado"] == "sin_respuesta" and fila["categoria_error"] == "sin_formato"
    malo = dict(p["gold"], Ana=1, Carla=3)
    fila = brazo_c.correr_problema(p, ClienteFalso(json.dumps(malo)), 2, 2)
    assert fila["resultado"] == "incorrecto" and fila["categoria_error"] == "incorrecta"
    assert fila["detectable"] == ERRORES_C["incorrecta"] == "no"


def test_costos():
    import costos
    filas = [
        {"brazo": "C", "resultado": "correcto", "tokens_entrada": "100", "tokens_salida": "50",
         "tiempo_llm_s": "2", "tiempo_solver_s": "0"},
        {"brazo": "C", "resultado": "incorrecto", "tokens_entrada": "100", "tokens_salida": "50",
         "tiempo_llm_s": "2", "tiempo_solver_s": "0"},
        {"brazo": "B", "resultado": "sin_respuesta", "tokens_entrada": "10", "tokens_salida": "10",
         "tiempo_llm_s": "1", "tiempo_solver_s": "0"},
    ]
    c = costos.costo_por_correcta(filas)
    assert c["C"]["intentos"] == 2 and c["C"]["correctas"] == 1
    assert c["C"]["tokens_totales"] == 300
    assert math.isclose(c["C"]["segundos_por_correcta"], 4.0)
    assert math.isinf(float(c["B"]["usd_por_correcta"]))
    assert costos.PRECIOS["fuente"] and costos.PRECIOS["fecha_consulta"]


def test_figuras_con_datos_falsos():
    subprocess.run([PY, str(AQUI / "datos_falsos.py")], check=True)
    salida = RAIZ / "fig" / "falso"
    subprocess.run([PY, str(AQUI / "figuras.py"), "--carpeta", str(RAIZ / "results" / "falso"),
                    "--salida", str(salida)], check=True)
    for nombre in ("precision_vs_dificultad.png", "costo_por_correcta.png",
                   "tiempo_llm_vs_solver.png", "iteraciones_bp.png", "taxonomia_b.png"):
        assert (salida / nombre).exists(), nombre
    assert leer(carpeta=RAIZ / "results" / "falso")


if __name__ == "__main__":
    pruebas = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    fallas = 0
    for t in pruebas:
        try:
            t()
            print(f"ok     {t.__name__}")
        except Exception as e:  # noqa: BLE001
            fallas += 1
            print(f"FALLA  {t.__name__}: {type(e).__name__}: {e}")
    print(f"{len(pruebas) - fallas}/{len(pruebas)} pruebas de Jalil pasan")
    sys.exit(1 if fallas else 0)
