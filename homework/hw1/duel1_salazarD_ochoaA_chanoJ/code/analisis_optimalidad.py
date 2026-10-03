"""Parte 1, análisis 1 y 4. RESPONSABLE: Daniel Salazar (con Claude).

Análisis 1: UCS y A* con heurística admisible devuelven el MISMO costo en las
80 instancias; BFS no, en costos no uniformes (grilla). Mostrar la instancia
donde BFS es subóptimo (camino, costo BFS vs óptimo, dibujo de la grilla).
En el 8-puzzle los costos son uniformes y BFS sí es óptimo: decirlo con la
condición, nunca "BFS es óptimo" a secas.

Análisis 4: factor de ramificación efectivo b* de A* con cada heurística:
N + 1 = 1 + b* + b*^2 + ... + b*^d, con N = expansiones y d = longitud de la
solución. Se resuelve por bisección. Reportar mediana [IQR] por nivel.

Salidas:
    results/optimalidad.csv, results/bfs_suboptimo.md,
    results/branching.csv, fig/branching.png
"""
from rutas import preparar_rutas

preparar_rutas()


def b_estrella(n_expansiones, profundidad, tol=1e-6):
    raise NotImplementedError  # TODO Daniel


def optimalidad():
    raise NotImplementedError  # TODO Daniel


def branching():
    raise NotImplementedError  # TODO Daniel


if __name__ == "__main__":
    optimalidad()
    branching()
