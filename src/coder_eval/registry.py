from typing import Callable, Any, TypedDict
from coder_eval import humaneval


class BenchmarkConfig(TypedDict):
    name: str
    fetch: Callable[[], list[dict[str, Any]]]
    columns: Callable[[], list[str]]
    row: Callable[[dict[str, Any]], list[str]]


BENCHMARK_CONFIG: dict[str, BenchmarkConfig] = {
    "humaneval": BenchmarkConfig(
        name="HumanEval",
        fetch=humaneval.fetch_tasks,
        columns=humaneval.table_columns,
        row=humaneval.row_from_task,
    ),
}
