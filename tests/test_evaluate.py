from pathlib import Path
from coder_eval.evaluate import create_results_dir, read_tasks, read_samples
import re
import json
import pytest
import typer


def test_create_results_dir_default(tmp_path: Path) -> None:
    """It should default to <path>/results/[timestamp]_<benchmark>_<model>/"""
    bench_path: Path = tmp_path / "benchmarks" / "custom-bench"
    bench_path.mkdir(parents=True)

    outdir: Path = create_results_dir(bench_path, None, "custom-bench", "test-model")

    assert outdir.exists()
    assert outdir.parent == bench_path / "results"
    assert re.match(
        r"\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}_custom-bench_test-model", outdir.name
    )


def test_create_results_dir_override(tmp_path: Path) -> None:
    """It should respect user-supplied output_dir and not add 'results/' nesting."""
    output_root: Path = tmp_path / "custom_results"
    output_root.mkdir(parents=True)

    outdir: Path = create_results_dir(
        Path("/any/path"), output_root, "mybench", "my-model"
    )

    assert outdir.exists()
    assert outdir.parent == output_root
    assert "mybench" in outdir.name
    assert "my-model" in outdir.name
    assert re.match(
        r"\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}_mybench_my-model", outdir.name
    )


def test_read_tasks_success(tmp_path: Path) -> None:
    """It should successfully read tasks.jsonl and return a dict mapping id to task."""
    tasks_file: Path = tmp_path / "tasks.jsonl"
    task1 = {
        "id": "task_1",
        "benchmark": "humaneval",
        "prompt": "def add(a, b):",
        "entry_point": "add",
        "reference_solution": "return a + b",
        "tests": ["assert add(1, 2) == 3"],
    }
    task2 = {
        "id": "task_2",
        "benchmark": "humaneval",
        "prompt": "def multiply(a, b):",
        "entry_point": "multiply",
        "reference_solution": "return a * b",
        "tests": ["assert multiply(2, 3) == 6"],
    }

    with tasks_file.open("w", encoding="utf-8") as f:
        f.write(json.dumps(task1) + "\n")
        f.write(json.dumps(task2) + "\n")

    tasks_data = read_tasks(tasks_file)

    assert len(tasks_data) == 2
    assert tasks_data["task_1"] == task1
    assert tasks_data["task_2"] == task2


def test_read_tasks_skips_empty_lines(tmp_path: Path) -> None:
    """It should skip empty lines in tasks.jsonl."""
    tasks_file: Path = tmp_path / "tasks.jsonl"
    task = {
        "id": "task_1",
        "benchmark": "humaneval",
        "prompt": "def add(a, b):",
        "entry_point": "add",
        "reference_solution": "return a + b",
        "tests": ["assert add(1, 2) == 3"],
    }

    with tasks_file.open("w", encoding="utf-8") as f:
        f.write("\n")
        f.write(json.dumps(task) + "\n")
        f.write("   \n")
        f.write("\n")

    tasks_data = read_tasks(tasks_file)

    assert len(tasks_data) == 1
    assert tasks_data["task_1"] == task


def test_read_tasks_file_not_found(tmp_path: Path) -> None:
    """It should raise typer.BadParameter when tasks file is not found."""
    tasks_file: Path = tmp_path / "nonexistent.jsonl"

    with pytest.raises(typer.BadParameter, match="Tasks file not found"):
        read_tasks(tasks_file)


def test_read_tasks_empty_file(tmp_path: Path) -> None:
    """It should raise typer.BadParameter when tasks.jsonl is empty."""
    tasks_file: Path = tmp_path / "tasks.jsonl"
    tasks_file.touch()

    with pytest.raises(typer.BadParameter, match="No tasks found in tasks.jsonl"):
        read_tasks(tasks_file)


def test_read_samples_success(tmp_path: Path) -> None:
    """It should successfully read samples.jsonl and return a list of samples."""
    samples_file: Path = tmp_path / "samples.jsonl"
    sample1 = {
        "task_id": "task_1",
        "model_name": "gpt-4",
        "completions": ["def add(a, b): return a + b"],
    }
    sample2 = {
        "task_id": "task_2",
        "model_name": "gpt-4",
        "completions": ["def multiply(a, b): return a * b"],
    }

    with samples_file.open("w", encoding="utf-8") as f:
        f.write(json.dumps(sample1) + "\n")
        f.write(json.dumps(sample2) + "\n")

    samples_data = read_samples(samples_file)

    assert len(samples_data) == 2
    assert samples_data[0] == sample1
    assert samples_data[1] == sample2


def test_read_samples_skips_empty_lines(tmp_path: Path) -> None:
    """It should skip empty lines in samples.jsonl."""
    samples_file: Path = tmp_path / "samples.jsonl"
    sample = {
        "task_id": "task_1",
        "model_name": "gpt-4",
        "completions": ["def add(a, b): return a + b"],
    }

    with samples_file.open("w", encoding="utf-8") as f:
        f.write("\n")
        f.write(json.dumps(sample) + "\n")
        f.write("   \n")
        f.write("\n")

    samples_data = read_samples(samples_file)

    assert len(samples_data) == 1
    assert samples_data[0] == sample


def test_read_samples_file_not_found(tmp_path: Path) -> None:
    """It should raise typer.BadParameter when samples file is not found."""
    samples_file: Path = tmp_path / "nonexistent.jsonl"

    with pytest.raises(typer.BadParameter, match="Samples file not found"):
        read_samples(samples_file)


def test_read_samples_empty_file(tmp_path: Path) -> None:
    """It should raise typer.BadParameter when samples.jsonl is empty."""
    samples_file: Path = tmp_path / "samples.jsonl"
    samples_file.touch()

    with pytest.raises(typer.BadParameter, match="No samples found in samples.jsonl"):
        read_samples(samples_file)
