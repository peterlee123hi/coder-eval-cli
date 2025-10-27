import typer
from typing import Any
from coder_eval.registry import BenchmarkConfig
from coder_eval.utils import get_benchmark_or_exit

app = typer.Typer(help="Create local version of a benchmark dataset.")


@app.callback(invoke_without_command=True)
def prepare(
    benchmark: str = typer.Option(..., help="Name of benchmark."),
    path: str = typer.Option(..., help="Path to store benchmark data."),
    tasks: str | None = typer.Option(
        None, help="Comma-separated list of task IDs to prepare."
    ),
):
    """Download or initialize a benchmark dataset."""
    typer.echo(f"Preparing {benchmark} at {path}")
    config: BenchmarkConfig = get_benchmark_or_exit(benchmark)
    if tasks:
        tasks_list: list[str] = [task.strip() for task in tasks.split(",")]

    benchmark_tasks: list[dict[str, Any]] = config["fetch"](tasks_list)
    config["prepare"](benchmark_tasks)
    typer.echo(f"✅ Prepared {len(benchmark_tasks)} tasks from {benchmark}")
