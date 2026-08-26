# Week 1 Studio — ELIZA vs. First Contact with a Real Model


**Deliverables:** all provided tests pass; `eliza.py` extended with a documented failure; `first_contact.md` with both transcripts and three answers.

> **Recap (5 min), cold-called.** *What did Turing replace "can machines think?" with, and why?* (Answer to have ready: an operational, testable game, the imitation game, because the original question is "too meaningless to deserve discussion.")

## Files in this folder

| File | Purpose | You edit it? |
|---|---|---|
| [`eliza.py`](eliza.py) | Given: the ELIZA engine, unchanged from the Session A notebook (6 rules, reflection map, fallback) | ❌ |
| [`prompts.json`](prompts.json) | Given: the exact inputs from the notebook. The demo conversation, the four failure probes, and the deduped `first_contact` set | ❌ |
| [`starter.py`](starter.py) | **Task 1:**  add three rules, an extended responder, and one declared failure case | ✅ |
| [`test_eliza.py`](test_eliza.py) | Provided tests, incl. `test_declared_failure_is_hollow` (watch a guarantee fail) | ❌ |

New files **you** create: `first_contact.md` (Task 2) and your committed `week01/eliza.py` (Task 1 docstring).

## Task 0: Confirm your backend (2 min)

One line in the shared channel: **which backend is your pair on** `ollama`, `api`, or `manual`? 

```bash
python -m aicourse.llm --list-backends
```

## Task 1: Extend ELIZA + provided tests (13 min)

Open `starter.py`. Fill three TODOs:

- `new_rules():` return **≥ 3 new** `(pattern, [templates])` rules (same shape as `eliza.RULES`). No duplicates of the base patterns; no pattern that matches the empty string.
- `extended_respond(text):` base rules first, then your new rules, then fallback. Reuse `eliza.reflect` for the pronoun swap; do not reinvent it.
- `failure_case():` return `(input_text, why_it_fails)` for **one deliberate failure**. A compound `"<clause A> and <clause B>"` sentence your ELIZA answers fluently while dropping clause B entirely.

Then:

```bash
python3 test_eliza.py
```

All five tests must pass. Two of them pin a *failure*:

- `test_base_eliza_ignores_second_clause:` on the given engine, the notebook's compound probe ("My mother is a doctor and my father is a lawyer") provably drops the second clause. First-match-wins means ELIZA has no model of the rest of the input.
- `test_declared_failure_is_hollow:` insists **your** declared failure reproduces exactly that drop. A test that expects failure is not a bug; being able to *predict* where ELIZA breaks is the skill.

**Commit** your work as `week01/eliza.py` with a docstring documenting the failure (paste the `why_it_fails` string from `failure_case()`), as the plan asks.

Fast-finishing pairs: *ELIZA felt plausible for about six exchanges in the demo. Which of your three new rules would survive a seventh, and which is the most brittle? Say why in one sentence.*

## Task 2. First contact: same prompts, two systems (30 min)

Send the **same** inputs to ELIZA and to the local model. The inputs live in `prompts.json` under `first_contact`, reuse them verbatim so the whole room compares the same failures.

```bash
python -m aicourse.llm --backend ollama --prompt "I am not feeling great about the exam"
```

Sketch (also in `starter.py`):

```python
import json
from aicourse.llm import LLM
from starter import extended_respond

prompts = json.load(open("prompts.json"))["first_contact"]
llm = LLM(backend="ollama")          # or run with --backend manual
for p in prompts:
    print("you  >", p)
    print("ELIZA>", extended_respond(p))
    print("LLM  >", llm.complete(p).text, "\n")
```

Record **both** transcripts in `first_contact.md`. If you are on `manual`, cap at the first **3** prompts and note it. Then answer, two or three sentences each:

1. Where does the LLM **obviously** beat ELIZA?
2. Find **one** input where the LLM's failure is *recognizably ELIZA-like* (fluent, on-topic, and hollow). This is harder, and it is the point.
3. Which system's failures are easier to predict **in advance**? Why does that matter if you have to ship one of them?


## Debrief (10 min)

- **The Duel Scorecard** ([`../../resources/duel-scorecard.md`](../../resources/duel-scorecard.md)). Score ELIZA vs. the local model together, out loud, across the eight axes.


