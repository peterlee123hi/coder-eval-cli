import typer
from pathlib import Path
from datetime import datetime

app = typer.Typer(help="Evaluate generated model outputs against benchmarks.")


def create_results_dir(path: Path, output_dir: Path | None, name: str) -> Path:
    """Create a results directory for the evaluation."""
    results_root = output_dir or (path / "results")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    outdir = results_root / f"{timestamp}_{name}"
    outdir.mkdir(parents=True, exist_ok=True)
    return outdir


@app.callback(invoke_without_command=True)
def evaluate(
    path: str = typer.Option(..., help="Path to benchmark directory."),
    samples: str = typer.Option(..., help="Path to JSONL file with model samples."),
    output_dir: str = typer.Option(None, help="Path to results directory."),
):
    """Evaluate generated samples."""
    typer.echo(f"Evaluating {samples} on benchmark at {path}")

    # TODO: Read samples.jsonl from args
    # TODO: Read tasks.jsonl from path/tasks.jsonl
    # TODO: Call evaluator from registry
    # TODO: By default, output results to path/results as specified by README (or output-dir if specified)
    # Alias is from tasks.jsonl and should match the folder name
    # TODO: Print results to console
