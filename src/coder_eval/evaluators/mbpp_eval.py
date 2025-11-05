from coder_eval.types import Task, Sample, SampleResult, ExecResult
from coder_eval.docker_utils import run_script


def evaluate(task: Task, sample: Sample) -> SampleResult:
    """Evaluate a MBPP task with completions and summarize results."""
    num_passed: int = 0
    num_failed: int = 0
    results: list[ExecResult] = []

    for completion in sample["completions"]:
        # Build runnable script
        full_script_parts: list[str] = [
            task["test_setup"],
            completion.strip(),
            "\n".join(task["tests"]),
        ]
        full_script: str = "\n\n".join([part for part in full_script_parts if part])

        exec_result: ExecResult = run_script(full_script)
        passed: bool = exec_result.get("returncode", 1) == 0

        results.append(exec_result)

        if passed:
            num_passed += 1
        else:
            num_failed += 1

    # Build summarized result
    summary: SampleResult = SampleResult(
        task_id=task["id"],
        model_name=sample["model_name"],
        passed_any=num_passed > 0,
        num_passed=num_passed,
        num_failed=num_failed,
        results=results,
    )

    return summary
