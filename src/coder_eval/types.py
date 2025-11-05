from typing import TypedDict, Callable


class Task(TypedDict):
    id: str
    benchmark: str
    prompt: str
    entry_point: str
    reference_solution: str
    tests: list[str]


class Sample(TypedDict):
    task_id: str
    model_name: str
    completions: list[str]


class ExecResult(TypedDict, total=False):
    script: str
    stdout: str
    stderr: str
    returncode: int
    exec_time: float
    error: str


class SampleResult(TypedDict, total=False):
    task_id: str
    model_name: str
    passed_any: bool
    num_passed: int
    num_failed: int
    results: list[ExecResult]


class BenchmarkConfig(TypedDict):
    name: str
    fetch: Callable[[], list[Task]]
    evaluate: Callable[[Task, Sample], SampleResult]
