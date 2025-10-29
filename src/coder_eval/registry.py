from coder_eval.types import BenchmarkConfig
from coder_eval.datasets import humaneval


BENCHMARK_CONFIG: dict[str, BenchmarkConfig] = {
    "humaneval": {
        "name": "HumanEval",
        "fetch": humaneval.fetch_tasks,
    },
}
