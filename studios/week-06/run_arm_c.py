import csv
import json
from pathlib import Path
from collections import Counter

from logic_lm import load_puzzles, parse_json, ParseError
from run_experiment import OllamaModel


def main():
    model = OllamaModel()

    puzzles = [
        p for p in load_puzzles()
        if not p.get("worked_example", False)
    ]

    counts = Counter()
    output_file = Path(__file__).resolve().parent / "results_arm_c.csv"

    with output_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["id", "category", "answer", "raw_response"],
        )
        writer.writeheader()
        file.flush()

        for index, puzzle in enumerate(puzzles, start=1):
            print(
                f"\n=== {puzzle['id']} ({index}/{len(puzzles)}) ===",
                flush=True,
            )

            prompt = (
                "Solve the following logic puzzle directly. "
                "Return only a JSON object mapping each entity name "
                "to its assigned value. "
                "Use entity names and values exactly as written "
                "in the puzzle. Use numbers for numeric values. "
                "Do not return a CSP, domains, or constraints.\n\n"
                'Example answer format: {"Ana": "green", '
                '"Bob": "blue", "Cara": "red"}\n\n'
                "Puzzle:\n" + puzzle["puzzle"]
            )

            reply = model.complete(prompt)
            answer = None

            try:
                answer = parse_json(reply)

                if not isinstance(answer, dict):
                    category = "invalid_format"
                elif all(
                    answer.get(name) == value
                    for name, value in puzzle["gold"].items()
                ):
                    category = "correct"
                else:
                    category = "incorrect"

            except ParseError:
                category = "invalid_format"

            counts[category] += 1

            writer.writerow({
                "id": puzzle["id"],
                "category": category,
                "answer": json.dumps(answer, ensure_ascii=False),
                "raw_response": reply,
            })
            file.flush()

            print("Resultado:", category, flush=True)
            print("Respuesta:", answer, flush=True)
            print("Esperada:", puzzle["gold"], flush=True)

    total = len(puzzles)

    print("\n=== RESULTADOS DEL BRAZO C ===")
    print(
        f"Aciertos: {counts['correct']}/{total} "
        f"({counts['correct'] / total:.1%})"
    )
    print("Incorrectos:", counts["incorrect"])
    print("Formato invalido:", counts["invalid_format"])
    print("Archivo:", output_file)


if __name__ == "__main__":
    main()