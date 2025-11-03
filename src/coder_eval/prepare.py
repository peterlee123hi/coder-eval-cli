from typing import Final
import typer
import json
from pathlib import Path
from coder_eval.types import Task, BenchmarkConfig
from coder_eval.utils import get_benchmark_or_exit

app = typer.Typer(help="Create local version of a benchmark dataset.")

GENERATE_SAMPLES_TEMPLATE: Final[
    str
] = """import json
from pathlib import Path

# Read tasks.jsonl
tasks_file = Path("tasks.jsonl")
with open(tasks_file) as f:
    tasks = [json.loads(line) for line in f]

# Write samples.jsonl
if tasks:
    first_task = tasks[0]
    sample = {
        "task_id": first_task["id"],
        "model_name": "gpt-4",
        "completions": [first_task["reference_solution"]],
    }

    samples_file = Path("samples.jsonl")
    with open(samples_file, "w") as f:
        f.write(json.dumps(sample) + "\\n")

    print("Generated samples.jsonl")
else:
    print("No tasks found in tasks.jsonl")
"""


@app.callback(invoke_without_command=True)
def prepare(
    benchmark: str = typer.Option(..., help="Name of benchmark."),
    path: str = typer.Option(..., help="Path to store benchmark data."),
):
    """Download or initialize a benchmark dataset."""
    config: BenchmarkConfig = get_benchmark_or_exit(benchmark)
    benchmark_name: str = config["name"]
    typer.echo(f"Preparing {benchmark_name} at {path}")

    tasks: list[Task] = config["fetch"]()
    typer.echo(f"✅ Prepared {len(tasks)} tasks from {benchmark_name}")

    # Write tasks.jsonl to path
    base_dir: Path = Path(path)
    base_dir.mkdir(parents=True, exist_ok=True)
    with open(base_dir / "tasks.jsonl", "w") as f:
        for task in tasks:
            f.write(json.dumps(task) + "\n")
    typer.echo(f"✅ Wrote {len(tasks)} tasks to {base_dir / 'tasks.jsonl'}")

    # Write generate_samples.py template to path
    with open(base_dir / "generate_samples.py", "w") as f:
        f.write(GENERATE_SAMPLES_TEMPLATE)
    typer.echo(f"✅ Wrote generate_samples.py to {base_dir / 'generate_samples.py'}")
