from coder_eval.types import BenchmarkConfig
from coder_eval.datasets import humaneval, mbpp
from coder_eval.evaluators import humaneval_eval, mbpp_eval


BENCHMARK_CONFIG: dict[str, BenchmarkConfig] = {
    "humaneval": BenchmarkConfig(
        name="HumanEval",
        fetch=humaneval.fetch_tasks,
        evaluate=humaneval_eval.evaluate,
    ),
    "mbpp": BenchmarkConfig(
        name="MBPP",
        fetch=mbpp.fetch_tasks,
        evaluate=mbpp_eval.evaluate,
    ),
}
