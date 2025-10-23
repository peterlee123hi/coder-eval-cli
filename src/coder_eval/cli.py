import typer
from coder_eval import prepare, evaluate, list_tasks

app = typer.Typer(help="Testing LLM coding agents on SWE benchmarks.")

app.add_typer(prepare.app, name="prepare")
app.add_typer(evaluate.app, name="evaluate")
app.add_typer(list_tasks.app, name="list-tasks")


def version_callback(value: bool):
    """Show version and exit."""
    from coder_eval import __version__

    if value:
        typer.echo(f"coder-eval-cli version {__version__}")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
):
    """coder-eval: Testing LLM coding agents on SWE benchmarks."""
    if not ctx.invoked_subcommand:
        typer.echo(ctx.get_help())
        raise typer.Exit()


if __name__ == "__main__":
    app()
