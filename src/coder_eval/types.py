from typing import TypedDict, Callable, Optional


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


class SampleResult(TypedDict, total=False):
    task_id: str
    model_name: str
    completion: str

    passed: bool
    num_passed: int
    num_failed: int

    stdout: Optional[str]
    stderr: Optional[str]
    exec_time: Optional[float]
    error: Optional[str]


class BenchmarkConfig(TypedDict):
    name: str
    fetch: Callable[[], list[Task]]
    evaluate: Callable[[Task, Sample], SampleResult]
