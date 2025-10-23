import typer

app = typer.Typer(help="Evaluate generated model outputs against benchmarks.")


@app.callback(invoke_without_command=True)
def evaluate(
    path: str = typer.Option(..., help="Path to benchmark directory."),
    samples: str = typer.Option(..., help="Path to JSONL file with model samples."),
):
    """Evaluate generated samples."""
    typer.echo(f"Evaluating {samples} on benchmark at {path}")
