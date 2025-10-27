from typing import Callable, Any, TypedDict
from coder_eval.datasets import humaneval
from coder_eval.evaluators import humaneval_eval


class BenchmarkConfig(TypedDict):
    name: str
    fetch: Callable[..., list[dict[str, Any]]]
    columns: Callable[[], list[str]]
    row: Callable[[dict[str, Any]], list[str]]
    evaluate: Callable[[list[dict[str, Any]], list[dict[str, Any]]], dict[str, Any]]
    prepare: Callable[[list[dict[str, Any]]], None]


BENCHMARK_CONFIG: dict[str, BenchmarkConfig] = {
    "humaneval": {
        "name": "HumanEval",
        "fetch": humaneval.fetch_tasks,
        "columns": humaneval.table_columns,
        "row": humaneval.row_from_task,
        "evaluate": humaneval_eval.evaluate_humaneval,
        "prepare": humaneval.prepare_tasks,
    },
}
