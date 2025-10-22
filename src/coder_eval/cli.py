import typer
from coder_eval import prepare, evaluate, list_tasks

app = typer.Typer(help="Evaluating LLM coding agents on SWE benchmarks.")

app.add_typer(prepare.app, name="prepare")
app.add_typer(evaluate.app, name="evaluate")
app.add_typer(list_tasks.app, name="list-tasks")


def version_callback(value: bool):
    """Show version and exit."""
    from coder_eval import __version__

    if value:
        typer.echo(f"coder-eval-cli version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
):
    """coder-eval: Evaluating LLM coding agents on SWE benchmarks."""
    pass


if __name__ == "__main__":
    app()
