from coder_eval.types import BenchmarkConfig
from coder_eval.datasets import humaneval
from coder_eval.evaluators import humaneval_eval


BENCHMARK_CONFIG: dict[str, BenchmarkConfig] = {
    "humaneval": {
        "name": "HumanEval",
        "fetch": humaneval.fetch_tasks,
        "evaluate": humaneval_eval.evaluate,
    },
}
