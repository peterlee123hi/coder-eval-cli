from unittest.mock import patch
from coder_eval.evaluators.humaneval_eval import evaluate
from coder_eval.types import Task, Sample, SampleResult


def test_evaluate_single_completion_passes() -> None:
    """It should return a summary when a single completion passes."""
    task: Task = {
        "id": "test_task_1",
        "benchmark": "humaneval",
        "prompt": "def add(a, b):",
        "entry_point": "add",
        "reference_solution": "return a + b",
        "tests": ["assert add(1, 2) == 3"],
    }
    sample: Sample = {
        "task_id": "test_task_1",
        "model_name": "test-model",
        "completions": ["    return a + b"],
    }

    mock_result: SampleResult = {
        "task_id": "test_task_1",
        "model_name": "test-model",
        "passed": True,
        "num_passed": 1,
        "num_failed": 0,
        "stdout": "",
        "stderr": None,
        "exec_time": 0.1,
    }

    with (
        patch(
            "coder_eval.evaluators.humaneval_eval.ensure_docker_image"
        ) as mock_ensure,
        patch(
            "coder_eval.evaluators.humaneval_eval.run_script", return_value=mock_result
        ) as mock_run,
    ):
        result = evaluate(task, sample)

    mock_ensure.assert_called_once()
    mock_run.assert_called_once()

    # Verify the script was built correctly
    call_args = mock_run.call_args
    assert call_args[1]["model_name"] == "test-model"
    assert call_args[1]["task_id"] == "test_task_1"
    script = call_args[1]["script"]
    assert "def add(a, b):" in script
    assert "return a + b" in script
    assert "assert add(1, 2) == 3" in script
    assert "check(add)" in script

    assert result["task_id"] == "test_task_1"
    assert result["model_name"] == "test-model"
    assert result["num_passed"] == 1
    assert result["num_failed"] == 0
    assert result["completion"] == "    return a + b"
    assert result.get("passed") is True


def test_evaluate_single_completion_fails() -> None:
    """It should return a summary when a single completion fails."""
    task: Task = {
        "id": "test_task_2",
        "benchmark": "humaneval",
        "prompt": "def multiply(a, b):",
        "entry_point": "multiply",
        "reference_solution": "return a * b",
        "tests": ["assert multiply(2, 3) == 6"],
    }
    sample: Sample = {
        "task_id": "test_task_2",
        "model_name": "test-model",
        "completions": ["    return a + b"],
    }

    mock_result: SampleResult = {
        "task_id": "test_task_2",
        "model_name": "test-model",
        "passed": False,
        "num_passed": 0,
        "num_failed": 1,
        "stdout": "",
        "stderr": "AssertionError",
        "exec_time": 0.1,
    }

    with (
        patch(
            "coder_eval.evaluators.humaneval_eval.ensure_docker_image"
        ) as mock_ensure,
        patch(
            "coder_eval.evaluators.humaneval_eval.run_script", return_value=mock_result
        ) as mock_run,
    ):
        result = evaluate(task, sample)

    mock_ensure.assert_called_once()
    mock_run.assert_called_once()

    assert result["task_id"] == "test_task_2"
    assert result["model_name"] == "test-model"
    assert result["num_passed"] == 0
    assert result["num_failed"] == 1
    assert result["completion"] == "    return a + b"
    assert result.get("passed") is False


def test_evaluate_multiple_completions_first_passes() -> None:
    """It should use first_pass when multiple completions and first one passes."""
    task: Task = {
        "id": "test_task_3",
        "benchmark": "humaneval",
        "prompt": "def subtract(a, b):",
        "entry_point": "subtract",
        "reference_solution": "return a - b",
        "tests": ["assert subtract(5, 3) == 2"],
    }
    sample: Sample = {
        "task_id": "test_task_3",
        "model_name": "test-model",
        "completions": [
            "    return a - b",
            "    return a + b",
            "    return a * b",
        ],
    }

    # First call passes, subsequent calls fail
    mock_results = [
        {
            "task_id": "test_task_3",
            "model_name": "test-model",
            "passed": True,
            "num_passed": 1,
            "num_failed": 0,
            "stdout": "",
            "stderr": None,
            "exec_time": 0.1,
        },
        {
            "task_id": "test_task_3",
            "model_name": "test-model",
            "passed": False,
            "num_passed": 0,
            "num_failed": 1,
            "stdout": "",
            "stderr": "AssertionError",
            "exec_time": 0.1,
        },
        {
            "task_id": "test_task_3",
            "model_name": "test-model",
            "passed": False,
            "num_passed": 0,
            "num_failed": 1,
            "stdout": "",
            "stderr": "AssertionError",
            "exec_time": 0.1,
        },
    ]

    with (
        patch("coder_eval.evaluators.humaneval_eval.ensure_docker_image"),
        patch(
            "coder_eval.evaluators.humaneval_eval.run_script",
            side_effect=mock_results,
        ) as mock_run,
    ):
        result = evaluate(task, sample)

    assert mock_run.call_count == 3

    assert result["task_id"] == "test_task_3"
    assert result["model_name"] == "test-model"
    assert result["num_passed"] == 1
    assert result["num_failed"] == 2
    # Should use first_pass completion
    assert result["completion"] == "    return a - b"
    assert result.get("passed") is True


def test_evaluate_multiple_completions_all_fail() -> None:
    """It should use last_fail when all completions fail."""
    task: Task = {
        "id": "test_task_4",
        "benchmark": "humaneval",
        "prompt": "def divide(a, b):",
        "entry_point": "divide",
        "reference_solution": "return a / b",
        "tests": ["assert divide(6, 2) == 3"],
    }
    sample: Sample = {
        "task_id": "test_task_4",
        "model_name": "test-model",
        "completions": [
            "    return a + b",
            "    return a - b",
            "    return a * b",
        ],
    }

    mock_results = [
        {
            "task_id": "test_task_4",
            "model_name": "test-model",
            "passed": False,
            "num_passed": 0,
            "num_failed": 1,
            "stdout": "",
            "stderr": "AssertionError",
            "exec_time": 0.1,
        },
        {
            "task_id": "test_task_4",
            "model_name": "test-model",
            "passed": False,
            "num_passed": 0,
            "num_failed": 1,
            "stdout": "",
            "stderr": "AssertionError",
            "exec_time": 0.1,
        },
        {
            "task_id": "test_task_4",
            "model_name": "test-model",
            "passed": False,
            "num_passed": 0,
            "num_failed": 1,
            "stdout": "",
            "stderr": "AssertionError",
            "exec_time": 0.1,
        },
    ]

    with (
        patch("coder_eval.evaluators.humaneval_eval.ensure_docker_image"),
        patch(
            "coder_eval.evaluators.humaneval_eval.run_script",
            side_effect=mock_results,
        ) as mock_run,
    ):
        result = evaluate(task, sample)

    assert mock_run.call_count == 3

    assert result["task_id"] == "test_task_4"
    assert result["model_name"] == "test-model"
    assert result["num_passed"] == 0
    assert result["num_failed"] == 3
    # Should use last_fail completion
    assert result["completion"] == "    return a * b"
    assert result.get("passed") is False


def test_evaluate_script_building() -> None:
    """It should build the script correctly from task components."""
    task: Task = {
        "id": "test_task_5",
        "benchmark": "humaneval",
        "prompt": "def func(x):\n    ",
        "entry_point": "func",
        "reference_solution": "return x * 2",
        "tests": ["assert func(5) == 10\n"],
    }
    sample: Sample = {
        "task_id": "test_task_5",
        "model_name": "test-model",
        "completions": ["return x * 2\n"],
    }

    mock_result: SampleResult = {
        "task_id": "test_task_5",
        "model_name": "test-model",
        "passed": True,
        "num_passed": 1,
        "num_failed": 0,
        "stdout": "",
        "stderr": None,
        "exec_time": 0.1,
    }

    with (
        patch("coder_eval.evaluators.humaneval_eval.ensure_docker_image"),
        patch(
            "coder_eval.evaluators.humaneval_eval.run_script", return_value=mock_result
        ) as mock_run,
    ):
        evaluate(task, sample)

    call_args = mock_run.call_args
    script = call_args[1]["script"]

    # Verify script components
    assert script.startswith("def func(x):")
    assert "return x * 2" in script
    assert "assert func(5) == 10" in script
    assert "if __name__ == '__main__':" in script
    assert "check(func)" in script
    # Verify whitespace is stripped properly
    assert "\n\n" in script  # Should have double newline between sections


def test_evaluate_empty_completions() -> None:
    """It should handle empty completions list gracefully."""
    task: Task = {
        "id": "test_task_6",
        "benchmark": "humaneval",
        "prompt": "def test():",
        "entry_point": "test",
        "reference_solution": "pass",
        "tests": ["assert test() is None"],
    }
    sample: Sample = {
        "task_id": "test_task_6",
        "model_name": "test-model",
        "completions": [],
    }

    with (
        patch("coder_eval.evaluators.humaneval_eval.ensure_docker_image"),
        patch("coder_eval.evaluators.humaneval_eval.run_script") as mock_run,
    ):
        result = evaluate(task, sample)

    # Should not call run_script if no completions
    mock_run.assert_not_called()

    assert result["task_id"] == "test_task_6"
    assert result["model_name"] == "test-model"
    assert result["num_passed"] == 0
    assert result["num_failed"] == 0
