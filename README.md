# CMP-4004 — Artificial Intelligence

**Classical Foundations, Modern Comparisons**

Universidad San Francisco de Quito · Colegio de Ciencias e Ingenierías

---

## What this course is

A traditional AI course: search, logic, planning, optimization, probabilistic
reasoning, and early machine learning. Every classical technique
is **measured against a modern LLM-based implementation of the same
task**.

The classical material is not history. It is the control group.

Students leave the course able to answer a question most practitioners cannot:
*given this problem, should I reach for an algorithm with guarantees, a language model, or a hybrid, and what evidence supports that choice?*

## The recurring finding

By roughly week 8, students will have generated their own evidence for the
course's central architectural claim:

> For problems with formal structure, a language model is usually the wrong
> **engine** and the right **front-end**. The strong pattern is
> natural language → formal model (via LLM) → verified solver → answer.

This is not an anti-LLM course, and it is not an LLM-hype course. It is a course
about knowing what you can prove.


## Setup

Everything runs on a student laptop with no GPU, no paid API, and no cloud
account. See [`resources/setup.md`](resources/setup.md).

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m aicourse.doctor      # verifies the whole toolchain
```

Students start with **[Week 0](weeks/week-00.md)**, a self-paced onboarding
week that gets the toolchain working and teaches programming *with* an LLM rather than chatting with one.

## Repository layout

```
course-en/
├── README.md                    ← you are here
├── syllabus.md                  Student-facing syllabus (English)
├── requirements.txt             Python dependencies
├── aicourse/                    The course harness (week 0 builds on this)
│   ├── llm.py                   Cached multi-backend LLM client
│   ├── cache.py                 Content-addressed response cache
│   ├── compare.py               The duel comparison harness
│   ├── doctor.py                Environment check
│   └── tests/                   31 tests — pytest aicourse/tests/
├── weeks/
│   ├── week-00.md               Async onboarding week (no source deck)
│   └── week-01.md … week-14.md  Instructor lesson plans
├── slides/
│   ├── README.md                Deck index, Marp rendering, conventions
│   └── week-01/ … week-14/
│       ├── deck.md              Marp slides for the Session A mini-lecture
│       └── images/              Figures extracted from the original .pptx
├── notebooks/
│   ├── README.md                Notebook index, runtimes, conventions
│   └── week-01-*.ipynb …        Runnable live-coding notebooks, one per week
├── projects/
│   ├── duel-1-search.md         16 %, due wk 6
│   ├── duel-2-formalizer.md     16 %, due wk 9
│   ├── duel-3-optimization.md   16 %, due wk 11
│   ├── capstone.md              20 %, due wk 14
│   └── checkpoints.md           12 % each, wks 7 and 13
└── resources/
    ├── setup.md                 Toolchain, incl. the three LLM backends
    ├── duel-scorecard.md        The rubric reused all 14 weeks
    ├── reading-list.md          Every reading, with links
    ├── ai-policy.md             AI use + the disclosure log
    ├── teaching-guide.md        Why the A/B split; virtual-classroom mechanics
    └── coverage-map.md          Original decks → these weeks; what was added/dropped
```

