import typer
from coder_eval.registry import BENCHMARK_CONFIG


def get_benchmark_or_exit(benchmark: str):
    if benchmark not in BENCHMARK_CONFIG:
        typer.echo(f"Benchmark '{benchmark}' not supported.")
        raise typer.Exit()

    return BENCHMARK_CONFIG[benchmark]
