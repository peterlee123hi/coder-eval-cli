from coder_eval.types import Task, Sample, SampleResult, ExecResult
from coder_eval.docker_utils import run_script, ensure_docker_image


def evaluate(task: Task, sample: Sample) -> SampleResult:
    """Evaluate a HumanEval task with completions and summarize results."""
    ensure_docker_image()

    num_passed: int = 0
    num_failed: int = 0
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

        exec_result: ExecResult = run_script(full_script)
        passed = exec_result.get("returncode", 1) == 0

        result: SampleResult = SampleResult(
            task_id=task["id"],
            model_name=sample["model_name"],
            completion=completion,
            passed=passed,
            stdout=exec_result.get("stdout", ""),
            stderr=exec_result.get("stderr", ""),
            exec_time=exec_result.get("exec_time", 0.0),
            error=exec_result.get("error", ""),
        )

        if passed:
            num_passed += 1
            if first_pass is None:
                first_pass = result
        else:
            num_failed += 1
            last_fail = result

    # Build a single summarized result
    summary: SampleResult = first_pass or last_fail or SampleResult()
    summary["task_id"] = task["id"]
    summary["model_name"] = sample["model_name"]
    summary["num_passed"] = num_passed
    summary["num_failed"] = num_failed

    return summary
