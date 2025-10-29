import typer
import json
from pathlib import Path
from coder_eval.types import Task, BenchmarkConfig
from coder_eval.utils import get_benchmark_or_exit

app = typer.Typer(help="Create local version of a benchmark dataset.")


@app.callback(invoke_without_command=True)
def prepare(
    benchmark: str = typer.Option(..., help="Name of benchmark."),
    path: str = typer.Option(..., help="Path to store benchmark data."),
):
    """Download or initialize a benchmark dataset."""
    typer.echo(f"Preparing {benchmark} at {path}")
    config: BenchmarkConfig = get_benchmark_or_exit(benchmark)

    tasks: list[Task] = config["fetch"]()
    typer.echo(f"✅ Prepared {len(tasks)} tasks from {benchmark}")

    # Write tasks.jsonl to path
    base_dir: Path = Path(path)
    with open(base_dir / "tasks.jsonl", "w") as f:
        for task in tasks:
            f.write(json.dumps(task) + "\n")
    typer.echo(f"✅ Wrote {len(tasks)} tasks to {base_dir / 'tasks.jsonl'}")

    # TODO: Write generate_samples.py to path
