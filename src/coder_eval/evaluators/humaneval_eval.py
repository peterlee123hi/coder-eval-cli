from coder_eval.types import Task, Sample, SampleResult
from coder_eval.docker_utils import run_script, ensure_docker_image


def evaluate(task: Task, sample: Sample) -> SampleResult:
    """Evaluate a HumanEval task with completions and summarize results."""
    ensure_docker_image()

    num_passed = 0
    num_failed = 0
    first_pass: SampleResult | None = None
    last_fail: SampleResult | None = None

    for completion in sample["completions"]:
        # Build runnable script
        full_script = (
            f"{task['prompt'].rstrip()}\n"
            f"{completion.rstrip()}\n\n"
            f"{task['tests'][0].strip()}\n\n"
            f"if __name__ == '__main__':\n"
            f"    check({task['entry_point']})\n"
        )

        result = run_script(
            script=full_script,
            model_name=sample["model_name"],
            task_id=task["id"],
        )
        result["completion"] = completion

        if result.get("passed"):
            num_passed += 1
            if first_pass is None:
                first_pass = result
        else:
            num_failed += 1
            last_fail = result

    # Build a single summarized result
    summary = first_pass or last_fail or SampleResult()
    summary["task_id"] = task["id"]
    summary["model_name"] = sample["model_name"]
    summary["num_passed"] = num_passed
    summary["num_failed"] = num_failed

    if first_pass:
        summary["completion"] = first_pass["completion"]
    elif last_fail:
        summary["completion"] = last_fail["completion"]

    return summary
