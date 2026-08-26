"""Provided tests for week-1 Task 1.

Run: ``python3 test_eliza.py``. Prints one line per test.

Most tests exercise YOUR extensions in ``starter.py`` and will report
"not implemented yet" until you fill the TODOs. One test —
``test_base_eliza_ignores_second_clause`` — pins a guarantee failing on the
*given* engine (it always runs), and ``test_declared_failure_is_hollow`` insists
your declared failure reproduces it. Watching a guarantee fail on purpose is how
you learn to predict failure — the currency of this course.
"""
import re
import sys
import random

import eliza
import starter as s

# Patterns already shipped in the base engine — Task 1a must not duplicate these.
BASE_PATTERNS = {p for p, _ in eliza.RULES}


def test_base_eliza_ignores_second_clause():
    """GUARANTEE FAIL (given engine). The notebook's canonical compound probe:
    ELIZA reacts to 'my mother' and the entire second clause is invisible."""
    random.seed(1)
    probe = "My mother is a doctor and my father is a lawyer"
    reply = eliza.respond(probe).lower()
    assert "mother" in reply, f"expected ELIZA to react to clause A, got: {reply!r}"
    for dropped in ("father", "lawyer", "doctor"):
        assert dropped not in reply, (
            f"ELIZA somehow surfaced {dropped!r} — the second clause was NOT "
            f"dropped, so this is not the first-match-wins failure: {reply!r}")
    print("  ok  base ELIZA drops the second clause of a compound sentence")


def test_new_rules_count_and_shape():
    rules = s.new_rules()
    assert isinstance(rules, list) and len(rules) >= 3, (
        f"Task 1a asks for >= 3 new rules; got {len(rules) if hasattr(rules,'__len__') else rules!r}")
    for pattern, templates in rules:
        assert isinstance(pattern, str) and pattern, "each pattern must be a non-empty regex string"
        re.compile(pattern)  # must be a valid regex
        assert isinstance(templates, list) and templates, "each rule needs >= 1 template string"
        assert all(isinstance(t, str) and t for t in templates), "templates must be non-empty strings"
        assert re.search(pattern, "") is None, (
            f"pattern {pattern!r} matches the empty string — it would fire on "
            "everything and shadow the fallback. Make it a real trigger.")
    print(f"  ok  new_rules(): {len(rules)} well-formed, non-empty-matching rules")


def test_new_rules_are_novel():
    for pattern, _ in s.new_rules():
        assert pattern not in BASE_PATTERNS, (
            f"pattern {pattern!r} duplicates a base rule — add something new")
    print("  ok  new_rules() does not duplicate the base engine's patterns")


def test_extended_respond_preserves_base_behavior():
    """Base rules keep priority: an 'I feel ...' input still gets the base
    reflection, with pronouns swapped, not a fallback and not a new rule."""
    random.seed(1)
    reply = s.extended_respond("I feel anxious most of the time").lower()
    assert reply.startswith("do you often feel"), (
        f"extended_respond must consult the base rules first; got: {reply!r}")
    assert "anxious" in reply, f"reflection dropped the content: {reply!r}"
    print("  ok  extended_respond preserves base behavior (base rules win)")


def test_declared_failure_is_hollow():
    """GUARANTEE FAIL (your code). Your declared failure_case() must be a
    compound sentence whose second clause ELIZA drops entirely."""
    text, why = s.failure_case()
    assert isinstance(text, str) and text, "failure_case must return an input string"
    assert isinstance(why, str) and why.strip(), "failure_case must explain the failure"
    assert " and " in text.lower(), (
        "the provided test pins the compound-sentence failure: use "
        "'<clause A> and <clause B>'")
    random.seed(1)
    reply = s.extended_respond(text).lower()
    _, second = text.lower().split(" and ", 1)
    content = [w for w in re.findall(r"[a-z]+", second) if len(w) >= 4]
    assert content, "clause B has no content words to drop — pick a richer sentence"
    surfaced = [w for w in content if w in reply or REFLECT_get(w) in reply]
    assert not surfaced, (
        f"clause B words {surfaced} surfaced in the reply {reply!r} — ELIZA "
        "actually used the second clause, so this is not an ELIZA-class drop. "
        "Pick an input where the second clause is genuinely ignored.")
    print(f"  ok  declared failure drops clause B entirely ({text!r})")


def REFLECT_get(word):
    return eliza.REFLECT.get(word, word)


TESTS = [
    test_base_eliza_ignores_second_clause,
    test_new_rules_count_and_shape,
    test_new_rules_are_novel,
    test_extended_respond_preserves_base_behavior,
    test_declared_failure_is_hollow,
]


def main():
    failed = 0
    for t in TESTS:
        try:
            t()
        except NotImplementedError:
            print(f"  --  {t.__name__}: starter TODO not implemented yet")
            failed += 1
        except AssertionError as e:
            print(f"  FAIL {t.__name__}: {e}")
            failed += 1
    if failed:
        print(f"\n{failed}/{len(TESTS)} failed")
        sys.exit(1)
    print(f"\nall {len(TESTS)} tests pass")


if __name__ == "__main__":
    main()
