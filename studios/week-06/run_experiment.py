import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

from logic_lm import worked_examples
from starter import solve_arm_b_with_refinement


class OllamaModel:
    def __init__(self, model="qwen2.5:3b"):
        self.model = model
        self.cache_dir = Path(__file__).resolve().parent / ".llm_cache"
        self.cache_dir.mkdir(exist_ok=True)

    def complete(self, prompt):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0,
                "seed": 42,
                "num_ctx": 4096,
                "num_predict": 2048,
            },
        }

        cache_key = hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode("utf-8")
        ).hexdigest()

        cache_file = self.cache_dir / f"{cache_key}.json"

        if cache_file.exists():
            try:
                record = json.loads(
                    cache_file.read_text(encoding="utf-8")
                )

                if (
                    not isinstance(record, dict)
                    or not isinstance(record.get("response"), str)
                ):
                    raise ValueError("La cache no contiene una respuesta valida")

            except (json.JSONDecodeError, UnicodeDecodeError, ValueError) as error:
                # Conservar el archivo dañado como evidencia.
                backup = cache_file.with_suffix(".invalid")
                number = 1

                while backup.exists():
                    backup = cache_file.with_suffix(f".invalid.{number}")
                    number += 1

                cache_file.rename(backup)

                print(
                    f"  Cache invalida: {error}\n"
                    f"  Respaldo: {backup.name}\n"
                    "  Se solicitara nuevamente esta respuesta.",
                    flush=True,
                )

            else:
                print("  Usando respuesta guardada.", flush=True)
                return record["response"]

        print("  Esperando respuesta de Ollama...", flush=True)

        request = Request(
            "http://127.0.0.1:11434/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request, timeout=600) as response:
            result = json.loads(response.read().decode("utf-8"))

        if not isinstance(result.get("response"), str):
            raise ValueError("Ollama no devolvio una respuesta de texto")

        record = {
            "backend": "ollama",
            "request": payload,
            "response": result["response"],
            "metadata": result,
        }

        # Escribir primero en un temporal para evitar una cache parcial.
        temporary_file = cache_file.with_suffix(".tmp")

        temporary_file.write_text(
            json.dumps(record, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        temporary_file.replace(cache_file)

        return result["response"]

def main():
    import csv
    from collections import Counter
    from logic_lm import load_puzzles, OK

    model = OllamaModel()

    puzzles = [
        puzzle
        for puzzle in load_puzzles()
        if not puzzle.get("worked_example", False)
    ]

    output_file = (
        Path(__file__).resolve().parent / "results_arm_b.csv"
    )

    without_refinement = Counter()
    with_refinement = Counter()

    with output_file.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "id",
                "without_refinement",
                "with_refinement",
                "attempts",
                "solution",
            ],
        )
        writer.writeheader()
        file.flush()

        for index, puzzle in enumerate(puzzles, start=1):
            print(
                f"\n=== {puzzle['id']} "
                f"({index}/{len(puzzles)}) ===",
                flush=True,
            )

            print("\nB sin refinamiento:", flush=True)

            first_category, _, _ = solve_arm_b_with_refinement(
                model,
                puzzle["puzzle"],
                gold=puzzle["gold"],
                max_retries=1,
            )

            print("\nB con refinamiento:", flush=True)

            final_category, solution, attempts = (
                solve_arm_b_with_refinement(
                    model,
                    puzzle["puzzle"],
                    gold=puzzle["gold"],
                    max_retries=3,
                )
            )

            without_refinement[first_category] += 1
            with_refinement[final_category] += 1

            writer.writerow({
                "id": puzzle["id"],
                "without_refinement": first_category,
                "with_refinement": final_category,
                "attempts": attempts,
                "solution": json.dumps(
                    solution, ensure_ascii=False
                ),
            })
            file.flush()

            print(
                f"\nResumen {puzzle['id']}: "
                f"{first_category} -> {final_category}",
                flush=True,
            )

    total = len(puzzles)

    print("\n=== RESULTADOS DEL BRAZO B ===")

    for label, counts in [
        ("Sin refinamiento", without_refinement),
        ("Con refinamiento", with_refinement),
    ]:
        correct = counts[OK]

        print(
            f"\n{label}: {correct}/{total} "
            f"({correct / total:.1%})"
        )

        for category in [
            "correct",
            "malformed_json",
            "valid_json_wrong_model",
            "valid_no_solution",
            "timeout",
        ]:
            print(f"  {category}: {counts[category]}")

    print(f"\nResultados guardados en: {output_file}")


if __name__ == "__main__":
    main()