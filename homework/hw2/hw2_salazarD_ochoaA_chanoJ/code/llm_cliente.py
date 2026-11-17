"""Cliente LLM común para los brazos B, B' y C.

Usa el cliente `aicourse` del curso (copiado en code/aicourse, el mismo del
deber 1) con la caché obligatoria en `.llm_cache/` de esta carpeta. Añade lo que
pide la instrumentación del HW2:

  * tokens de entrada y salida (Ollama los da como prompt_eval_count y eval_count)
  * el tiempo del LLM medido en la llamada ORIGINAL, aunque ahora venga de la
    caché (si no, una segunda corrida diría que el LLM tardó 0 s)

Uso:
    from llm_cliente import ClienteLLM
    llm = ClienteLLM()                      # modelo y temperatura de config.py
    r = llm.llamar("prompt...", semilla=1)
    r.texto, r.tokens_entrada, r.tokens_salida, r.tiempo_llm_s, r.cache, r.error

Variables de entorno: AICOURSE_MODEL (por defecto el de config.py).
"""
from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import config  # noqa: E402
from aicourse.cache import cache_key  # noqa: E402
from aicourse.llm import LLM  # noqa: E402

CACHE = AQUI.parent / ".llm_cache"
MODELO = os.environ.get("AICOURSE_MODEL", config.MODELO)


@dataclass
class RespuestaLLM:
    texto: str
    tokens_entrada: int
    tokens_salida: int
    tiempo_llm_s: float
    cache: bool
    modelo: str
    error: str | None = None


class ClienteLLM:
    def __init__(self, modelo: str = MODELO, backend: str = "ollama",
                 temperatura: float = config.TEMPERATURA, timeout: float = 300.0):
        self.modelo = modelo
        self.temperatura = temperatura
        self._llm = LLM(backend=backend, model=modelo, cache_dir=str(CACHE),
                        temperature=temperatura, timeout=timeout)

    def llamar(self, prompt: str, semilla: int = 0) -> RespuestaLLM:
        r = self._llm.complete(prompt, seed=semilla)
        tiempo = r.elapsed
        if r.cached:
            key = cache_key(self._llm.backend, self.modelo, prompt, self.temperatura, semilla)
            archivo = CACHE / key[:2] / f"{key}.json"
            try:
                guardado = json.loads(archivo.read_text(encoding="utf-8"))
                tiempo = float(guardado.get("elapsed", 0.0))
            except (OSError, ValueError):
                tiempo = 0.0
        meta = r.meta or {}
        return RespuestaLLM(
            texto=r.text or "",
            tokens_entrada=int(meta.get("prompt_eval_count", 0) or 0),
            tokens_salida=int(meta.get("eval_count", 0) or 0),
            tiempo_llm_s=tiempo,
            cache=r.cached,
            modelo=self.modelo,
            error=r.error,
        )


class ClienteFalso:
    """Para probar código sin Ollama: responde siempre `texto`. Sus resultados
    NO se reportan."""

    def __init__(self, texto: str = "{}"):
        self.texto = texto
        self.modelo = "falso"

    def llamar(self, prompt: str, semilla: int = 0) -> RespuestaLLM:
        return RespuestaLLM(self.texto, len(prompt) // 4, len(self.texto) // 4, 0.0, False, "falso")
