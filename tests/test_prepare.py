import json
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest
import typer
from coder_eval.prepare import prepare
from coder_eval.types import Task, BenchmarkConfig


def test_prepare_successful(tmp_path: Path, capsys) -> None:
    """Test successful preparation of a benchmark."""
    # Create mock tasks
    mock_tasks: list[Task] = [
        {
            "id": "test_task_1",
            "benchmark": "humaneval",
            "prompt": "def add(a, b):",
            "entry_point": "add",
            "reference_solution": "return a + b",
            "tests": ["assert add(1, 2) == 3"],
        },
        {
            "id": "test_task_2",
            "benchmark": "humaneval",
            "prompt": "def multiply(a, b):",
            "entry_point": "multiply",
            "reference_solution": "return a * b",
            "tests": ["assert multiply(2, 3) == 6"],
        },
    ]

    # Create mock fetch function
    mock_fetch = MagicMock(return_value=mock_tasks)

    # Create mock benchmark config
    mock_config: BenchmarkConfig = {
        "name": "HumanEval",
        "fetch": mock_fetch,
        "evaluate": MagicMock(),
    }

    # Mock get_benchmark_or_exit to return our mock config
    benchmark_path = tmp_path / "benchmarks" / "test-bench"

    with patch("coder_eval.prepare.get_benchmark_or_exit", return_value=mock_config):
        prepare(benchmark="humaneval", path=str(benchmark_path))

    # Verify directory was created
    assert benchmark_path.exists()

    # Verify tasks.jsonl was created
    tasks_file = benchmark_path / "tasks.jsonl"
    assert tasks_file.exists()

    # Verify tasks were written correctly
    with open(tasks_file) as f:
        lines = f.readlines()
        assert len(lines) == len(mock_tasks)
        for i, line in enumerate(lines):
            task = json.loads(line.strip())
            assert task == mock_tasks[i]

    # Verify output messages
    captured = capsys.readouterr()
    assert "Preparing humaneval" in captured.out
    assert f"at {benchmark_path}" in captured.out
    assert f"✅ Prepared {len(mock_tasks)} tasks from humaneval" in captured.out
    assert f"✅ Wrote {len(mock_tasks)} tasks to" in captured.out
    assert "tasks.jsonl" in captured.out

    # Verify fetch was called
    mock_fetch.assert_called_once()


def test_prepare_empty_tasks(tmp_path: Path, capsys) -> None:
    """Test preparation with no tasks."""
    mock_config: BenchmarkConfig = {
        "name": "EmptyBench",
        "fetch": MagicMock(return_value=[]),
        "evaluate": MagicMock(),
    }

    benchmark_path = tmp_path / "benchmarks" / "empty-bench"

    with patch("coder_eval.prepare.get_benchmark_or_exit", return_value=mock_config):
        prepare(benchmark="emptybench", path=str(benchmark_path))

    # Verify directory was created
    assert benchmark_path.exists()

    # Verify tasks.jsonl was created (even if empty)
    tasks_file = benchmark_path / "tasks.jsonl"
    assert tasks_file.exists()

    # Verify file is empty
    with open(tasks_file) as f:
        content = f.read()
        assert content == ""

    # Verify output messages
    captured = capsys.readouterr()
    assert "✅ Prepared 0 tasks" in captured.out
    assert "✅ Wrote 0 tasks" in captured.out


def test_prepare_invalid_benchmark(tmp_path: Path) -> None:
    """Test preparation with invalid benchmark name."""
    benchmark_path = tmp_path / "benchmarks" / "invalid-bench"

    with patch("coder_eval.prepare.get_benchmark_or_exit", side_effect=typer.Exit()):
        with pytest.raises(typer.Exit):
            prepare(benchmark="invalidbench", path=str(benchmark_path))

    # Verify directory was not created
    assert not benchmark_path.exists()


def test_prepare_creates_directory(tmp_path: Path) -> None:
    """Test that prepare creates the directory if it doesn't exist."""
    mock_tasks: list[Task] = [
        {
            "id": "test_task_1",
            "benchmark": "humaneval",
            "prompt": "def test():",
            "entry_point": "test",
            "reference_solution": "pass",
            "tests": ["assert True"],
        },
    ]

    mock_config: BenchmarkConfig = {
        "name": "TestBench",
        "fetch": MagicMock(return_value=mock_tasks),
        "evaluate": MagicMock(),
    }

    # Use a path that doesn't exist
    benchmark_path = tmp_path / "new" / "nested" / "path"
    assert not benchmark_path.exists()

    with patch("coder_eval.prepare.get_benchmark_or_exit", return_value=mock_config):
        prepare(benchmark="testbench", path=str(benchmark_path))

    # Verify directory was created
    assert benchmark_path.exists()
    assert (benchmark_path / "tasks.jsonl").exists()


def test_prepare_tasks_jsonl_format(tmp_path: Path) -> None:
    """Test that tasks.jsonl is formatted correctly with one JSON object per line."""
    mock_tasks: list[Task] = [
        {
            "id": "task1",
            "benchmark": "humaneval",
            "prompt": "def func1():",
            "entry_point": "func1",
            "reference_solution": "return 1",
            "tests": ["assert func1() == 1"],
        },
        {
            "id": "task2",
            "benchmark": "humaneval",
            "prompt": "def func2():",
            "entry_point": "func2",
            "reference_solution": "return 2",
            "tests": ["assert func2() == 2", "assert func2() != 1"],
        },
    ]

    mock_config: BenchmarkConfig = {
        "name": "TestBench",
        "fetch": MagicMock(return_value=mock_tasks),
        "evaluate": MagicMock(),
    }

    benchmark_path = tmp_path / "benchmarks" / "format-test"

    with patch("coder_eval.prepare.get_benchmark_or_exit", return_value=mock_config):
        prepare(benchmark="testbench", path=str(benchmark_path))

    tasks_file = benchmark_path / "tasks.jsonl"

    # Verify each line is valid JSON and matches the task
    with open(tasks_file) as f:
        lines = f.readlines()
        assert len(lines) == len(mock_tasks)

        for i, line in enumerate(lines):
            # Each line should end with newline (except possibly the last)
            assert line.endswith("\n") or i == len(lines) - 1

            # Parse JSON from line
            task = json.loads(line.strip())
            assert task == mock_tasks[i]

            # Verify all required fields
            assert "id" in task
            assert "benchmark" in task
            assert "prompt" in task
            assert "entry_point" in task
            assert "reference_solution" in task
            assert "tests" in task
            assert isinstance(task["tests"], list)
