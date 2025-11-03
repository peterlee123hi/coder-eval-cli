GENERATE_SAMPLES_TEMPLATE: str = """import json
from pathlib import Path

# Read tasks.jsonl
tasks_file = Path("tasks.jsonl")
with open(tasks_file) as f:
    tasks = [json.loads(line) for line in f]

# Write samples.jsonl
if tasks:
    first_task = tasks[0]
    sample = {
        "task_id": first_task["id"],
        "model_name": "gpt-4",
        "completions": [first_task["reference_solution"]],
    }

    samples_file = Path("samples.jsonl")
    with open(samples_file, "w") as f:
        f.write(json.dumps(sample) + "\\n")

    print("Generated samples.jsonl")
else:
    print("No tasks found in tasks.jsonl")
"""
