import typer

app = typer.Typer(help="List available tasks in a benchmark.")


@app.command()
def list_tasks(
    benchmark: str = typer.Option(None, help="Name of benchmark."),
):
    """List tasks for a benchmark."""
    if benchmark:
        typer.echo(f"Listing tasks for benchmark: {benchmark}")
    else:
        typer.echo("Please specify --benchmark.")
