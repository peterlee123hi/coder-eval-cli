from typing import Callable, Any, TypedDict
from coder_eval.datasets import humaneval
from coder_eval.evaluators import humaneval_eval


class BenchmarkConfig(TypedDict):
    name: str
    fetch: Callable[[], list[dict[str, Any]]]
    evaluate: Callable[[list[dict[str, Any]], list[dict[str, Any]]], dict[str, Any]]
    prepare: Callable[[list[dict[str, Any]]], None]


BENCHMARK_CONFIG: dict[str, BenchmarkConfig] = {
    "humaneval": {
        "name": "HumanEval",
        "fetch": humaneval.fetch_tasks,
        "evaluate": humaneval_eval.evaluate_humaneval,
        "prepare": humaneval.prepare_tasks,
    },
}
