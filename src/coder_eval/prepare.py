import typer

app = typer.Typer(help="Prepare benchmark datasets or custom repositories.")


@app.callback(invoke_without_command=True)
def prepare(
    benchmark: str = typer.Option(
        None, help="Name of benchmark, e.g. mbpp or swe-bench-verified."
    ),
    path: str = typer.Option(..., help="Path to store benchmark data."),
    tasks: int = typer.Option(None, help="Number of tasks to load (if applicable)."),
    repo: str = typer.Option(None, help="Custom repository to clone as a benchmark."),
):
    """Download or initialize a benchmark dataset."""
    typer.echo(f"Preparing {benchmark or repo} at {path}")
