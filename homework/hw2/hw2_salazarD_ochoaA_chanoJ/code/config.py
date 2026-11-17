"""Protocolo experimental común (lo usan los brazos B, B' y C por igual).

Si cambian algo aquí, cambia para todos: avisen en el grupo antes de tocarlo.
"""
MODELO = "qwen2.5:3b"          # el del curso (resources/setup.md); 3 mil millones de parámetros
TEMPERATURA = 0.7              # > 0 para que las repeticiones midan varianza de verdad
SEMILLAS = (0, 1, 2)           # 3 repeticiones por problema y brazo
MAX_REFINAMIENTOS = 3          # B': hasta 3 reintentos después del primer intento
LIMITE_LLAMADAS_SOLVER = 200_000
LIMITE_SEGUNDOS_SOLVER = 10.0
