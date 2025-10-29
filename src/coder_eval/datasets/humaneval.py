from datasets import load_dataset
from coder_eval.types import Task


def fetch_tasks() -> list[Task]:
    """Fetch and normalize tasks from Hugging Face."""
    dataset = load_dataset("openai/openai_humaneval", split="test", revision="7dce605")
    tasks: list[Task] = []
    for row in dataset:
        tasks.append(
            {
                "id": row["task_id"],
                "benchmark": "humaneval",
                "prompt": row["prompt"],
                "entry_point": row["entry_point"],
                "reference_solution": row["canonical_solution"],
                "tests": [row["test"]],
            }
        )

    return tasks
