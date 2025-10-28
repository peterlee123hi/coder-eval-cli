from datasets import load_dataset


def fetch_tasks() -> list[dict]:
    """Fetch and normalize tasks from Hugging Face."""
    dataset = load_dataset("evalplus/humanevalplus", split="test", revision="d32357c")
    tasks: list[dict] = []
    for row in dataset:
        tasks.append(
            {
                "id": row["task_id"],
                "benchmark": "humaneval",
                "prompt": row["prompt"],
                "entry_point": row.get("entry_point"),
                "reference": row.get("canonical_solution"),
                "test_code": row.get("test"),
            }
        )

    return tasks


def prepare_tasks(tasks: list[dict]) -> None:
    """Prepare tasks for local evaluation."""
    pass
