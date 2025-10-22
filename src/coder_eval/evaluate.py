import typer

app = typer.Typer(help="Evaluate generated model outputs against benchmarks.")


@app.command()
def evaluate(
    path: str = typer.Option(..., help="Path to benchmark directory."),
    samples: str = typer.Option(..., help="Path to JSONL file with model samples."),
):
    """Evaluate model-generated samples."""
    typer.echo(f"Evaluating {samples} on benchmark at {path} ...")
