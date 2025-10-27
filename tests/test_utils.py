import pytest
import typer
from coder_eval.utils import get_benchmark_or_exit
from coder_eval.registry import BENCHMARK_CONFIG


def test_valid_benchmark():
    name = next(iter(BENCHMARK_CONFIG))
    result = get_benchmark_or_exit(name)
    assert result == BENCHMARK_CONFIG[name]


def test_none_benchmark(capsys):
    with pytest.raises(typer.Exit):
        get_benchmark_or_exit(None)
    out = capsys.readouterr().out
    assert "Available benchmarks:" in out


def test_invalid_benchmark(capsys):
    with pytest.raises(typer.Exit):
        get_benchmark_or_exit("fakebench")
    out = capsys.readouterr().out
    assert "not supported" in out
