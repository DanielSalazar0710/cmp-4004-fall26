"""Week 2 studio - Task 1 and LLM socket."""
import re

from vacuum import simple_reflex, model_based


def goal_based(goal=(False, False)):
    """Return an agent that plans toward an explicit goal and then stops."""
    target_clean = [not dirty for dirty in goal]
    state = {"clean": [False, False], "loc": None}

    def agent(percept):
        loc, dirty = percept
        state["loc"] = loc

        if dirty:
            state["clean"][loc] = True
            return "Suck"

        state["clean"][loc] = True
        if state["clean"] == target_clean:
            return "NoOp"

        other = 1 - loc
        return "Right" if other == 1 else "Left"

    return agent


def utility_based(move_cost=1, suck_cost=2, clean_reward=3):
    """Return an agent that maximizes immediate net utility."""
    state = {"clean": [False, False], "loc": None}

    def agent(percept):
        loc, dirty = percept
        state["loc"] = loc

        if dirty:
            state["clean"][loc] = True
            return "Suck"

        state["clean"][loc] = True
        other = 1 - loc
        crossing_gain = -move_cost
        if not state["clean"][other] and crossing_gain > 0:
            return "Right" if other == 1 else "Left"
        return "NoOp"

    return agent


PROMPT = """You control a vacuum robot in a 2-room world.
Rooms 0 and 1. Each is Clean or Dirty.
Actions: Left, Right, Suck, NoOp.
History of (percept, action) so far:
{history}
Current percept: location={loc}, status={status}
Reply with exactly one action word and nothing else."""

VALID_ACTIONS = ("Left", "Right", "Suck", "NoOp")


def parse_action(raw, failures=None):
    """Turn model text into one valid action, logging malformed replies."""
    text = str(raw).strip()
    match = re.search(r"\b(left|right|suck|noop|no\s*op)\b", text, re.I)
    if match:
        token = match.group(1).lower().replace(" ", "")
        return {"left": "Left", "right": "Right", "suck": "Suck",
                "noop": "NoOp"}[token]
    if failures is not None:
        failures.append(text)
    return None


def _format_history(history):
    if not history:
        return "(none)"
    return "\n".join(f"{percept} -> {action}" for percept, action in history)


def llm_agent(model=None, fallback="NoOp", failures=None, retries=1):
    """Return an LLM policy plugged into the same percept -> action socket."""
    if model is None:
        from aicourse.llm import LLM
        model = LLM()

    history = []
    failures = failures if failures is not None else []

    def agent(percept):
        loc, dirty = percept
        prompt = PROMPT.format(history=_format_history(history),
                               loc=loc,
                               status="Dirty" if dirty else "Clean")
        action = None
        for _ in range(retries + 1):
            response = model.complete(prompt)
            action = parse_action(getattr(response, "text", response), failures)
            if action is not None:
                break
        if action is None:
            action = fallback
        history.append((percept, action))
        return action

    return agent


if __name__ == "__main__":
    from tournament import tournament

    tournament({
        "reflex": lambda: simple_reflex,
        "model": model_based,
        "goal": goal_based,
        "utility": utility_based,
    })
