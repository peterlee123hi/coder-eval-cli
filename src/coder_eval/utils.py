import typer
from coder_eval.registry import BENCHMARK_CONFIG


def get_benchmark_or_exit(benchmark: str | None):
    if benchmark is None:
        typer.echo("Available benchmarks:")
        for name in BENCHMARK_CONFIG:
            typer.echo(f"- {name}")
        raise typer.Exit()

    if benchmark not in BENCHMARK_CONFIG:
        typer.echo(f"Benchmark '{benchmark}' not supported.")
        raise typer.Exit()

    return BENCHMARK_CONFIG[benchmark]
