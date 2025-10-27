import typer
from typing import Any
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from coder_eval.registry import BenchmarkConfig
from coder_eval.utils import get_benchmark_or_exit

app = typer.Typer(help="List available tasks in a benchmark.")
console = Console()


def render_table(
    tasks: list[dict], config: BenchmarkConfig, start: int, end: int
) -> None:
    """Render a static page of the table."""
    table = Table(
        title=f"{config['name']} tasks {start + 1}-{min(end, len(tasks))}",
        expand=True,
        show_lines=True,
    )
    for col in config["columns"]():
        table.add_column(col, overflow="fold", no_wrap=False)

    for task in tasks[start:end]:
        table.add_row(*config["row"](task))

    console.print(table)


def paginate_tasks(tasks: list[dict], config: BenchmarkConfig, page_size: int) -> None:
    """Paginate through tasks with static pages."""
    idx: int = 0
    total: int = len(tasks)
    pages: int = (total + page_size - 1) // page_size

    while True:
        render_table(tasks, config, idx, idx + page_size)
        current_page: int = idx // page_size + 1
        console.print(
            Panel(
                f"[N] next  [B] back  [Q] quit    Page {current_page}/{pages}",
                style="dim",
            )
        )

        cmd: str = input("> ").strip().lower() or "n"
        if cmd == "n" and idx + page_size < total:
            idx += page_size
        elif cmd == "b" and idx - page_size >= 0:
            idx -= page_size
        elif cmd == "q":
            typer.echo("👋 Exiting task viewer.")
            break
        elif cmd == "":
            continue
        else:
            typer.echo("⚠️ Invalid input. Use N, B, or Q.")


@app.callback(invoke_without_command=True)
def list_tasks(
    benchmark: str = typer.Option(
        ...,
        help="Name of benchmark (mbpp, humaneval, apps, swe-bench-verified).",
    ),
    page_size: int = typer.Option(20, help="Number of rows per page."),
) -> None:
    """List tasks for a benchmark."""
    config: BenchmarkConfig = get_benchmark_or_exit(benchmark)
    tasks: list[dict[str, Any]] = config["fetch"]()
    typer.echo(f"✅ Loaded {len(tasks)} tasks from {benchmark}")
    paginate_tasks(tasks, config, page_size)
