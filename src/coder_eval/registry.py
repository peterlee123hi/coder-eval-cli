from typing import Callable, Any, TypedDict
from coder_eval.datasets import humaneval


class BenchmarkConfig(TypedDict):
    name: str
    fetch: Callable[[], list[dict[str, Any]]]


BENCHMARK_CONFIG: dict[str, BenchmarkConfig] = {
    "humaneval": {
        "name": "HumanEval",
        "fetch": humaneval.fetch_tasks,
    },
}
