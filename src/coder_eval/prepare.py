import typer
from typing import Any
from coder_eval.registry import BenchmarkConfig
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

    tasks: list[dict[str, Any]] = config["fetch"]()
    config["prepare"](tasks)
    typer.echo(f"✅ Prepared {len(tasks)} tasks from {benchmark}")

    # TODO: Write dockerfile (with task-level folders with artifacts)
    # TODO: Write tasks.jsonl
