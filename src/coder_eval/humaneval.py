from datasets import load_dataset


def fetch_tasks() -> list[dict]:
    """Fetch and normalize tasks from Hugging Face."""
    dataset = load_dataset("openai_humaneval", split="test")
    tasks = []

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


def table_columns() -> list[str]:
    return ["ID", "Prompt"]


def row_from_task(task: dict) -> list[str]:
    return [task["id"], f"{task['prompt'][:160]}..."]
