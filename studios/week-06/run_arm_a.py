import csv
import json
from pathlib import Path

from csp import backtrack_search
from logic_lm import build_csp, load_puzzles


def make_spec(names, values, different=False, pins=(), exclusions=()):
    """Construye dominios y restricciones a partir del enunciado."""
    names = names.split()

    constraints = []

    if different:
        constraints.append({
            "type": "alldiff",
            "vars": names,
        })

    for variable, value in pins:
        constraints.append({
            "type": "eq",
            "a": variable,
            "b": value,
        })

    for variable, other in exclusions:
        constraints.append({
            "type": "neq",
            "a": variable,
            "b": other,
        })

    return {
        "variables": {
            name: list(values)
            for name in names
        },
        "constraints": constraints,
    }


def build_models():
    # Modelos explicitos: no se leen los campos "spec" ni "gold"
    # para construir las restricciones.
    return {
        "p06": make_spec(
            "red silver black", [1, 2, 3], True,
            pins=[("black", 1)],
            exclusions=[("red", 3)],
        ),
        "p07": make_spec(
            "Ada Ben Cy Dee", [1, 2, 3, 4], True,
            pins=[("Ben", 1), ("Dee", 4)],
            exclusions=[("Ada", 1), ("Ada", 2)],
        ),
        "p08": make_spec(
            "A B C", ["white", "gray"],
            pins=[("A", "white")],
            exclusions=[("B", "A"), ("C", "B")],
        ),
        "p09": make_spec(
            "Novel Poems Essays Manual Comic", [1, 2, 3, 4, 5], True,
            pins=[("Novel", 1), ("Comic", 5), ("Essays", 3)],
            exclusions=[("Poems", 2)],
        ),
        "p10": make_spec(
            "Dishes Laundry Vacuum Trash", ["Mon", "Tue", "Wed", "Thu"],
            True,
            pins=[("Dishes", "Mon"), ("Vacuum", "Thu")],
            exclusions=[("Trash", "Tue")],
        ),
        "p11": make_spec(
            "X Y Z", ["teal", "olive", "plum"], True,
            pins=[("Y", "teal")],
            exclusions=[("X", "teal"), ("X", "olive")],
        ),
        "p12": make_spec(
            "P Q R S", [1, 2, 3, 4], True,
            pins=[("R", 2)],
            exclusions=[("Q", 1), ("S", 1), ("S", 3)],
        ),
        "p13": make_spec(
            "Al Bo Cy Di Ed", [1, 2, 3, 4, 5], True,
            pins=[("Al", 1), ("Ed", 5), ("Cy", 2)],
            exclusions=[("Bo", 2), ("Bo", 3)],
        ),
        "p14": make_spec(
            "Lamp1 Lamp2 Lamp3", ["on", "off"],
            pins=[("Lamp1", "on")],
            exclusions=[("Lamp2", "Lamp1"), ("Lamp3", "Lamp2")],
        ),
        "p15": make_spec(
            "N E S W", ["red", "blue", "green", "yellow"], True,
            pins=[("N", "red"), ("S", "green")],
            exclusions=[("E", "blue"), ("E", "green")],
        ),
        "p16": make_spec(
            "Tom Uma Val", ["A", "B", "C"], True,
            pins=[("Uma", "A")],
            exclusions=[("Tom", "B")],
        ),
        "p17": make_spec(
            "S1 S2 S3 S4", ["up", "down"],
            pins=[("S1", "up")],
            exclusions=[("S2", "S1"), ("S3", "S2"), ("S4", "S3")],
        ),
        "p18": make_spec(
            "Ana Bea Cam Dan Eli", [1, 2, 3, 4, 5], True,
            pins=[("Eli", 1), ("Bea", 2)],
            exclusions=[
                ("Ana", 1), ("Ana", 3), ("Ana", 5),
                ("Ana", 2), ("Cam", 5),
            ],
        ),
        "p19": make_spec(
            "Cup1 Cup2 Cup3", ["tea", "milk"],
            pins=[("Cup1", "tea")],
            exclusions=[("Cup2", "tea"), ("Cup3", "Cup2")],
        ),
        "p20": make_spec(
            "W X Y Z", ["red", "blue", "green", "black"], True,
            pins=[("W", "red"), ("Y", "black")],
            exclusions=[("X", "blue")],
        ),
    }


def main():
    models = build_models()
    puzzles = [
        p for p in load_puzzles()
        if not p.get("worked_example", False)
    ]

    output_file = Path(__file__).resolve().parent / "results_arm_a.csv"
    correct = 0

    with output_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["id", "category", "calls", "solution"],
        )
        writer.writeheader()

        for puzzle in puzzles:
            csp = build_csp(models[puzzle["id"]])

            solution, counter = backtrack_search(
                csp,
                use_fc=True,
                use_mrv=True,
                limit=200_000,
            )

            # gold solo se consulta despues de resolver.
            if solution == "TIMEOUT":
                category = "timeout"
            elif solution is None:
                category = "no_solution"
            elif solution == puzzle["gold"]:
                category = "correct"
                correct += 1
            else:
                category = "incorrect"

            print(puzzle["id"], category, solution)

            writer.writerow({
                "id": puzzle["id"],
                "category": category,
                "calls": counter["calls"],
                "solution": json.dumps(solution, ensure_ascii=False),
            })

    print(
        f"\nAciertos A: {correct}/{len(puzzles)} "
        f"({correct / len(puzzles):.1%})"
    )
    print("Archivo:", output_file)


if __name__ == "__main__":
    main()