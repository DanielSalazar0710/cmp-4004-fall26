"""Week 6 studio — starter (model a CSP, then build the Logic-LM arm-B loop).

You fill in two things. Run ``python3 test_csp.py`` as you go.

  Task 1  scheduling_csp()               -- model the school-schedule CSP (graded).
  Task 2  solve_arm_b_with_refinement()  -- the LLM->CSP pipeline + refinement loop.

The provided tests include ``test_lcv_can_hurt`` and
``test_plain_backtracking_blows_up`` -- both assert that a technique which
"should" help does *not*, on the notebook's HARD Sudoku. That is not a broken
test. LCV is a heuristic gamble that sometimes costs more than it saves, and plain
backtracking is exponential; watching a guarantee (or a hoped-for speedup) fail
once is how you learn it was never unconditional. See README.
"""
from csp import CSP, backtrack_search


# ---- Task 1: model the school-schedule CSP ----------------------------------
# From the deck: assign each activity to a distinct period, and "sports cannot be
# scheduled after lunch." This is a CSP straight out of the notebook's own class:
# all activities take DISTINCT periods (an all-different over a complete neighbour
# graph), and the sports variable's domain is pre-restricted to morning periods.
#
# The instance below is fixed so the tests are deterministic. You supply the
# *modelling*: the domains (with the sports restriction) and the neighbour graph.

ACTIVITIES = ["Math", "English", "Science", "Sports", "Art", "Music"]
PERIODS = [1, 2, 3, 4, 5, 6]        # the school day, in order
LUNCH_AFTER = 3                     # periods strictly greater than 3 are afternoon
AFTERNOON = [p for p in PERIODS if p > LUNCH_AFTER]   # [4, 5, 6]
SPORTS = "Sports"                   # the one activity barred from the afternoon


def scheduling_csp():
    domains = {}

    for activity in ACTIVITIES:
        if activity == SPORTS:
            domains[activity] = {
                period for period in PERIODS
                if period <= LUNCH_AFTER
            }
        else:
            domains[activity] = set(PERIODS)

    neighbors = {}

    for activity in ACTIVITIES:
        neighbors[activity] = {
            other for other in ACTIVITIES
            if other != activity
        }

    return CSP(ACTIVITIES, domains, neighbors)


def run_ablation(make_csp):
    """Convenience (provided): print the four-configuration ablation table for a
    factory that returns a fresh CSP each call. Use it to report Task 1's table."""
    import time
    configs = [
        ("plain backtracking",   dict()),
        ("+ forward checking",   dict(use_fc=True)),
        ("+ MRV",                dict(use_fc=True, use_mrv=True)),
        ("+ LCV",                dict(use_fc=True, use_mrv=True, use_lcv=True)),
        ("+ AC-3 preprocessing", dict(use_fc=True, use_mrv=True, use_ac3=True)),
    ]
    print(f"  {'configuration':<24}{'calls':>10}{'time':>10}{'solved':>9}")
    print("  " + "-" * 53)
    for label, kw in configs:
        csp = make_csp()
        t0 = time.perf_counter()
        result, counter = backtrack_search(csp, **kw)
        dt = time.perf_counter() - t0
        status = "TIMEOUT" if result == "TIMEOUT" else ("yes" if result else "no")
        print(f"  {label:<24}{counter['calls']:>10,}{dt:>9.4f}s{status:>9}")


# ---- Task 2: the Logic-LM arm-B pipeline + self-refinement loop -------------
# The plumbing is provided in logic_lm.py: MODEL_PROMPT, parse_json, build_csp,
# classify_arm_b, and the puzzle bank. YOU write the prompt wiring around your
# local model and the self-refinement loop the plan asks for.
#
# The full bank of 20 natural-language puzzles ships in puzzles.json; load it with
# logic_lm.load_puzzles(). Five are marked worked_example (logic_lm.worked_examples())
# -- fully-worked starters you can inspect and use as few-shot fuel. Run the three
# arms over all 20; report solve rate per arm and arm B's failure taxonomy.
#
# This function needs a live model, so the provided test suite does NOT run it.
# Validate it against the worked examples (each has a `gold` answer) before turning
# your LLM loose on the rest of the bank.

def solve_arm_b_with_refinement(model, puzzle, gold=None, max_retries=3):
    from logic_lm import (
        classify_arm_b,
        MALFORMED,
        NO_SOLUTION,
    )

    if max_retries < 1:
        raise ValueError("max_retries debe ser al menos 1")

    import json
    from logic_lm import worked_examples

    example = worked_examples()[0]

    prompt = (
        "Translate a logic puzzle into a CSP. Do not solve it.\n"
        "Return only a JSON object with variables and constraints.\n\n"
        "Rules:\n"
        "- variables maps EACH actual entity name to its domain.\n"
        "- A domain is a flat list of possible values.\n"
        "- Do not use placeholder keys such as name, domain or values.\n"
        "- Every variable referenced in a constraint must be defined.\n"
        "- alldiff uses vars: a list of variable names.\n"
        "- eq uses a: a variable name, b: a literal domain value.\n"
        "- neq uses a: a variable name, b: another variable or a "
        "literal domain value.\n"
        "- Use one alldiff constraint for an all-different group; "
        "do not also list every pair as neq.\n\n"
        "Worked example:\n"
        + example["puzzle"]
        + "\nCorrect CSP translation:\n"
        + json.dumps(example["spec"], ensure_ascii=False)
        + "\n\nNow translate this NEW puzzle:\n"
        + puzzle
    )

    for attempt in range(1, max_retries + 1):
        print(f"  Intento {attempt}/{max_retries}", flush=True)

        reply = model.complete(prompt)
        error_detail = ""

        try:
            category, solution = classify_arm_b(reply, gold=gold)

        except (TypeError, KeyError, ValueError, AttributeError) as error:
            category, solution = MALFORMED, None
            error_detail = f"{type(error).__name__}: {error}"
            print(f"  CSP invalido: {error_detail}", flush=True)

        print(f"  Categoria: {category}", flush=True)

        if category not in (MALFORMED, NO_SOLUTION):
            return category, solution, attempt

        if attempt == max_retries:
            return category, solution, attempt

        if category == MALFORMED:
            feedback = (
                "Your previous response was not valid JSON or did not "
                "follow the required CSP structure. "
                "The variables field must be a non-empty object mapping "
                "variable names to non-empty domains. "
                "Each domain must be a flat list of strings or numbers, "
                "never nested lists or objects. "
                'Example: "Ana": ["red", "green", "blue"]. '
                "The constraints field must be a list of objects. "
                "Constraint fields a and b must be single strings or "
                "numbers, not lists. For alldiff, use a vars list "
                "containing variable names."
            )

            if error_detail:
                feedback += f" Technical error: {error_detail}"

        else:
            feedback = (
                "The solver found no solution for your CSP. "
                "Check whether your constraints contradict the original "
                "puzzle. Correct the translation without removing any "
                "restrictions required by the puzzle."
            )

        prompt += (
            f"\n\nPrevious response:\n{reply}\n\n"
            f"Error: {feedback}\n"
            "Translate the original puzzle again. "
            "Use only the supported constraint types: alldiff, neq, eq. "
            "Return only the complete corrected JSON."
        )


if __name__ == "__main__":
    # Smoke test for Task 1: solve the schedule and show sports lands before lunch.
    try:
        csp = scheduling_csp()
    except NotImplementedError:
        print("  scheduling_csp not implemented yet")
    else:
        sol, counter = backtrack_search(csp, use_fc=True, use_mrv=True)
        print(f"  solved in {counter['calls']} calls:")
        for act in ACTIVITIES:
            print(f"    {act:<9} period {sol[act]}")
        print(f"  sports period = {sol[SPORTS]}  (lunch after {LUNCH_AFTER})")
        print("\n  ablation on this instance:")
        run_ablation(scheduling_csp)
