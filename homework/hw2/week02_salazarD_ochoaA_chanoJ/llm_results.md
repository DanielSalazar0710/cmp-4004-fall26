# LLM Results - Week 02

## Setup

- Backend: `ollama`
- Model: `qwen2.5:1.5b`
- Interface: `from aicourse.llm import LLM`
- Cache: `.llm_cache/`
- Configurations: 3, capped because local Ollama was slow
- Steps per configuration: 20
- Reproducibility run: first configuration repeated 5 times

## Backend check

```text
Python import: ok
LLM backend: ollama (qwen2.5:1.5b)
Response: 'Suck'
.llm_cache/ writable
```

## Experiment replay

The run below was replayed from `.llm_cache/`, so it made 0 new model calls.
The cache contains the original model responses used for the measurement.

```text
model,qwen2.5:1.5b
configs,3
steps,20
solved,3/3
total_utility,256
calls_total,160
calls_made,0
cache_hits,160
median_latency_seconds,0.000
p95_latency_seconds,0.009
parse_failures,0
repeat_distinct_sequences,1/5
```

## Cached model-call latency

Across the cached Week 2 LLM prompts:

```text
cached_responses,58
median_original_elapsed_seconds,3.152
p95_original_elapsed_seconds,3.673
```

## Rows

```text
dirt,loc,utility,final_dirt,actions
(True, True),0,74,(False, False),Suck Right Right Left Right Left Right Right Suck Right Right Right Right Right Right Right Right Right Right Right
(True, True),1,83,(False, False),Suck Right Right Right Left Suck Right Right Right Right Right Right Right Right Right Right Right Right Right Right
(True, False),0,99,(False, False),Suck Right Right Left Right Left Right Right Right Right Right Right Right Right Right Right Right Right Right Right
```

## Result

The LLM agent solved the 3 capped configurations, but its action sequences are not efficient. It often keeps choosing movement actions after the world is already clean. This keeps the main lesson visible: a valid action is not the same as a good policy.
