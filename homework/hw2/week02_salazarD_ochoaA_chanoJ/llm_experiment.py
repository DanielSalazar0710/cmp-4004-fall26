"""Run the Week 2 LLM agent experiment through aicourse.llm.LLM."""
import time

from aicourse.llm import LLM
from starter import llm_agent
from tournament import CLEAN_REWARD, MOVE_COST, SUCK_COST, load_configs
from vacuum import VacuumWorld

MODEL = "qwen2.5:1.5b"
CONFIG_LIMIT = 3
STEPS = 20


def run_trace(make_agent, dirt, loc, steps=STEPS):
    agent = make_agent()
    world = VacuumWorld(dirt, loc)
    actions = []
    utility = 0
    for _ in range(steps):
        action = agent(world.percept())
        actions.append(action)
        if action == "Suck":
            utility -= SUCK_COST
        elif action in ("Left", "Right"):
            utility -= MOVE_COST
        world.step(action)
        utility += CLEAN_REWARD * sum(not d for d in world.dirt)
    return actions, world, utility


def main():
    configs = load_configs()[:CONFIG_LIMIT]
    model = LLM(model=MODEL, temperature=0.0, timeout=120.0)
    failures = []
    rows = []
    latencies = []
    calls = 0

    for dirt, loc in configs:
        print(f"running config dirt={dirt} loc={loc} ...", flush=True)

        def make_agent(model=model, failures=failures):
            return llm_agent(model=model, failures=failures, retries=1)

        before = time.perf_counter()
        actions, world, utility = run_trace(make_agent, dirt, loc)
        elapsed = time.perf_counter() - before
        calls += STEPS
        latencies.append(elapsed / STEPS)
        rows.append({
            "dirt": dirt,
            "loc": loc,
            "utility": utility,
            "final_dirt": tuple(world.dirt),
            "actions": actions,
        })

    repeated = []
    repeat_config = configs[0]
    for _ in range(5):
        print(f"running reproducibility repeat {len(repeated) + 1}/5 ...",
              flush=True)

        def make_agent(model=model, failures=failures):
            return llm_agent(model=model, failures=failures, retries=1)

        before = time.perf_counter()
        actions, world, utility = run_trace(make_agent, repeat_config[0], repeat_config[1])
        elapsed = time.perf_counter() - before
        calls += STEPS
        latencies.append(elapsed / STEPS)
        repeated.append(tuple(actions))

    distinct_sequences = len(set(repeated))
    total_utility = sum(row["utility"] for row in rows)
    solved = sum(1 for row in rows if row["final_dirt"] == (False, False))
    median_latency = sorted(latencies)[len(latencies) // 2]
    p95_latency = sorted(latencies)[int(len(latencies) * 0.95) - 1]

    print(f"model,{MODEL}")
    print(f"configs,{len(configs)}")
    print(f"steps,{STEPS}")
    print(f"solved,{solved}/{len(configs)}")
    print(f"total_utility,{total_utility}")
    print(f"calls_total,{calls}")
    print(f"calls_made,{model.calls_made}")
    print(f"cache_hits,{calls - model.calls_made}")
    print(f"median_latency_seconds,{median_latency:.3f}")
    print(f"p95_latency_seconds,{p95_latency:.3f}")
    print(f"parse_failures,{len(failures)}")
    print(f"repeat_distinct_sequences,{distinct_sequences}/5")
    print()
    print("dirt,loc,utility,final_dirt,actions")
    for row in rows:
        actions = " ".join(row["actions"])
        print(f"{row['dirt']},{row['loc']},{row['utility']},{row['final_dirt']},{actions}")
    print()
    print("parse failure samples")
    for failure in failures[:5]:
        print(repr(failure))


if __name__ == "__main__":
    main()
