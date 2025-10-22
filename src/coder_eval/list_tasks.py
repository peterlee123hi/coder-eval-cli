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

    # TODO: implement default show 20 rows. Press N for next page. Press Q to quit.
    # TODO: --limit to dump N tasks to stdout
    # TODO: --all to dump all tasks to stdout
