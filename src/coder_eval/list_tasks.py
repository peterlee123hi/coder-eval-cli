import typer
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from coder_eval.registry import BENCHMARK_CONFIG, BenchmarkConfig

app = typer.Typer(help="List available tasks in a benchmark.")
console = Console()


def render_table(
    tasks: list[dict], config: BenchmarkConfig, start: int, end: int
) -> None:
    """Render a static page of the table."""
    table = Table(
        title=f"{config['name']} tasks {start + 1}-{min(end, len(tasks))}",
        expand=True,
        show_lines=False,
    )
    for col in config["columns"]():
        table.add_column(col, overflow="fold", no_wrap=False)

    for task in tasks[start:end]:
        table.add_row(*config["row"](task))

    console.print(table)


def paginate_tasks(tasks: list[dict], config: BenchmarkConfig, page_size: int) -> None:
    """Paginate through tasks with static pages."""
    idx = 0
    total = len(tasks)
    pages = (total + page_size - 1) // page_size

    while True:
        render_table(tasks, config, idx, idx + page_size)
        current_page = idx // page_size + 1
        console.print(
            Panel(
                f"[N] next  [B] back  [Q] quit    Page {current_page}/{pages}",
                style="dim",
            )
        )

        cmd = input("> ").strip().lower() or "n"
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
        None,
        help="Name of benchmark (mbpp, humaneval, apps, swe-bench-verified, livecodebench).",
    ),
    page_size: int = typer.Option(20, help="Number of rows per page."),
) -> None:
    """List tasks for a benchmark."""
    if benchmark not in BENCHMARK_CONFIG:
        typer.echo(f"Benchmark '{benchmark}' not supported.")
        raise typer.Exit()

    config = BENCHMARK_CONFIG[benchmark]
    tasks = config["fetch"]()
    total = len(tasks)
    typer.echo(f"✅ Loaded {total} tasks from {benchmark}")

    paginate_tasks(tasks, config, page_size)
