from typing import TypedDict, Callable


class Task(TypedDict):
    id: str
    benchmark: str
    prompt: str
    entry_point: str
    solution: str
    tests: list[str]


class BenchmarkConfig(TypedDict):
    name: str
    fetch: Callable[[], list[Task]]
