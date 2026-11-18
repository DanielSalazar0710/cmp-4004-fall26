"""Arma la carpeta limpia de entrega para el PR al repo del profe.

Copia solo lo que pide la consigna (REPORT, code, problems, results/*.csv,
fig/*.png, taxonomy.md, .llm_cache, AI_LOG) y deja fuera el material interno
del equipo (INDICACIONES, datos y figuras falsos, pruebas de aceptación,
corridas de prueba con los ejemplos, referencias).

    python code/entregar.py <destino>
    # ej.: python code/entregar.py ..\\salazar     (homework/hw2/salazar)
Imprime la lista de archivos y avisa si falta algo obligatorio.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

ORIGEN = Path(__file__).resolve().parent.parent

INCLUIR = ["REPORT.md", "taxonomy.md", "AI_LOG.md", "README.md", "requirements.txt",
           ".gitignore", "code", "problems", "results", "fig", ".llm_cache",
           "hw2_salazarD_ochoaA_chanoJ.ipynb", "hw2_salazarD_ochoaA_chanoJ.html"]
EXCLUIR_NOMBRES = {"__pycache__", "falso", "test_jalil.py", "datos_falsos.py", "entregar.py", "log_brazo_b.txt", "log_brazo_c.txt"}
EXCLUIR_SUFIJOS = ("_ejemplos.csv", "_ejemplos.jsonl", "_ejemplos.md", "_parcial.csv", "_parcial.jsonl")
OBLIGATORIOS = ["REPORT.md", "taxonomy.md", "AI_LOG.md", "results/brazo_a.csv", "results/brazo_b.csv",
                "results/brazo_c.csv", "fig/precision_vs_dificultad.png"]


def _ignorar(directorio, nombres):
    return [n for n in nombres if n in EXCLUIR_NOMBRES or n.endswith(EXCLUIR_SUFIJOS) or "_ejemplos_" in n]


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    destino = Path(sys.argv[1]).resolve()
    if destino.exists() and any(destino.iterdir()):
        print(f"{destino} ya existe y no está vacía; bórrala o elige otra.")
        return 1
    destino.mkdir(parents=True, exist_ok=True)
    for nombre in INCLUIR:
        src = ORIGEN / nombre
        if not src.exists():
            continue
        if src.is_dir():
            shutil.copytree(src, destino / nombre, ignore=_ignorar)
        else:
            shutil.copy2(src, destino / nombre)
    faltan = [o for o in OBLIGATORIOS if not (destino / o).exists()]
    pngs = list((destino / "fig").glob("*.png")) if (destino / "fig").exists() else []
    archivos = [p for p in destino.rglob("*") if p.is_file()]
    cache = sum(1 for p in archivos if ".llm_cache" in p.parts)
    print(f"{len(archivos)} archivos en {destino} ({cache} de .llm_cache)")
    for p in sorted(archivos):
        if ".llm_cache" not in p.parts:
            print("  ", p.relative_to(destino))
    # Revisión de tono: nada de notas internas ni de mensajes dirigidos a alguien.
    # (AI_LOG.md sí declara el uso de IA, como pide la política del curso; no se revisa aquí.)
    prohibido = ["[JALIL]", "TODO Jalil", "TODO Andretty", "INDICACIONES", "_(pendiente",
                 "Claude", "DATO FALSO", "Corríjanlos", "avisen"]
    for p in archivos:
        if ".llm_cache" in p.parts or p.name == "AI_LOG.md" or "aicourse" in p.parts:
            continue
        if p.suffix not in (".py", ".md", ".json", ".txt"):
            continue
        texto = p.read_text(encoding="utf-8", errors="ignore")
        for frase in prohibido:
            if frase in texto:
                faltan.append(f"{p.relative_to(destino)} contiene {frase!r}")
    if len(pngs) < 3:
        faltan.append(f"al menos 3 figuras (hay {len(pngs)})")
    if faltan:
        print("FALTA:", faltan)
        return 1
    print("Carpeta de entrega completa.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
