from datasets import load_dataset
from coder_eval.types import Task


def fetch_tasks() -> list[Task]:
    """Fetch and normalize tasks from Hugging Face."""
    dataset = load_dataset(
        "google-research-datasets/mbpp",
        "sanitized",
        split="test",
        revision="4bb6404",
    )

    tasks: list[Task] = []
    for row in dataset:
        test_setup: str = (
            "\n".join(row.get("test_imports", [])) if row.get("test_imports") else ""
        )
        tasks.append(
            {
                "id": f"{row['task_id']}",
                "benchmark": "mbpp",
                "prompt": row["prompt"],
                "reference_solution": row["code"],
                "tests": row["test_list"],
                "test_setup": test_setup,
            }
        )

    return tasks
