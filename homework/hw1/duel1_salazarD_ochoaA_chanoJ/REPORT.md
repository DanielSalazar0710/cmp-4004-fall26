# Duel 1 — Búsqueda clásica contra un LLM

**Equipo:** Daniel Salazar, Andretty Ochoa y Jalil Chano · CMP-4004 · USFQ

> Borrador. Cada sección indica quién la escribe. Límite: 2 000 palabras sin contar tablas ni leyendas. Las cifras salen de `results/`; ninguna se escribe a mano.

## 1. Qué medimos y cómo *(Daniel)*

Dominios, bancos (semilla 20260807), 4 niveles × 10 instancias, timeout de 30 s, máquina y modelo (`qwen2.5:3b`, temperatura 0, semilla 0).

## 2. The Duel Scorecard *(Daniel, con datos de todos)*

| Eje | Clásico (A*) | LLM | Herramienta | Evidencia |
|---|---|---|---|---|
| 1 Corrección | | | | `results/…` |
| 2 Garantía | | | | — |
| 3 Costo | | | | |
| 4 Latencia (mediana / p95) | | | | |
| 5 Reproducibilidad | | | | `results/llm_reproducibilidad.csv` |
| 6 Escalado | | | | `fig/escalado_optimalidad.png` |
| 7 Interpretabilidad | | | | — |
| 8 Modo de falla | | | | |

## 3. Parte 1: comparación clásica

### 3.1 Optimalidad: UCS = A*, y BFS cuando los costos no son uniformes *(Daniel)*

### 3.2 Dominancia de Manhattan sobre misplaced *(Andretty)*

### 3.3 Romper la admisibilidad: h × 3 *(Andretty)*

### 3.4 Factor de ramificación efectivo b* *(Daniel)*

## 4. Parte 2: el duelo

### 4.1 Brazo LLM: fallas por categoría y escalado *(Jalil)*

### 4.2 Reproducibilidad *(Jalil)*

### 4.3 Brazo con herramienta *(Daniel)*

## 5. Where we may have been unfair *(todos; cada uno aporta al menos un punto propio)*

## 6. Lo que nuestra evidencia no permite afirmar *(todos)*
