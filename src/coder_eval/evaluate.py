import json
import typer
from pathlib import Path
from datetime import datetime
from coder_eval.utils import get_benchmark_or_exit
from coder_eval.types import Task, BenchmarkConfig, Sample, SampleResult

app = typer.Typer(help="Evaluate generated model outputs against benchmarks.")


def create_results_dir(
    path: Path, output_dir: Path | None, benchmark: str, model: str
) -> Path:
    """Create a results directory for the evaluation."""
    results_root: Path = output_dir or (path / "results")
    timestamp: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    outdir: Path = results_root / f"{timestamp}_{benchmark}_{model}"
    outdir.mkdir(parents=True, exist_ok=True)
    return outdir


def read_tasks(path: Path) -> dict[str, Task]:
    """Read tasks.jsonl from path."""
    try:
        with path.open("r", encoding="utf-8") as f:
            tasks_data: dict[str, Task] = {}
            for line in f:
                if line.strip():
                    task: Task = json.loads(line.strip())
                    tasks_data[task["id"]] = task
    except FileNotFoundError as exc:
        raise typer.BadParameter(f"Tasks file not found: {path}") from exc
    if not tasks_data:
        raise typer.BadParameter("No tasks found in tasks.jsonl")
    return tasks_data


def read_samples(path: Path) -> list[Sample]:
    """Read samples.jsonl from path."""
    try:
        with path.open("r", encoding="utf-8") as f:
            samples_data: list[Sample] = [
                json.loads(line) for line in f if line.strip()
            ]
    except FileNotFoundError as exc:
        raise typer.BadParameter(f"Samples file not found: {path}") from exc
    if not samples_data:
        raise typer.BadParameter("No samples found in samples.jsonl")
    return samples_data


@app.callback(invoke_without_command=True)
def evaluate(
    path: str = typer.Option(..., help="Path to benchmark directory."),
    samples: str = typer.Option(..., help="Path to JSONL file with model samples."),
    output_dir: str = typer.Option(None, help="Path to results directory."),
):
    """Evaluate generated samples."""
    typer.echo(f"Evaluating {samples} on benchmark at {path}")

    # Read tasks.jsonl from path
    tasks_path: Path = Path(path) / "tasks.jsonl"
    tasks_data: dict[str, Task] = read_tasks(tasks_path)
    typer.echo(f"✅ Read {len(tasks_data)} tasks from {tasks_path}")

    # Get benchmark config
    benchmark_name: str = next(iter(tasks_data.values()))["benchmark"]
    benchmark_config: BenchmarkConfig = get_benchmark_or_exit(benchmark_name)

    # Read samples.jsonl
    samples_path: Path = Path(samples)
    samples_data: list[Sample] = read_samples(samples_path)
    typer.echo(f"✅ Read {len(samples_data)} samples from {samples_path}")

    # Call evaluator from registry
    results: list[SampleResult] = []
    processed_task_ids: set[str] = set()
    for sample_idx, sample in enumerate(samples_data):
        if sample["task_id"] in processed_task_ids:
            typer.echo(
                f"⚠️ Task ID '{sample['task_id']}' appears again in sample {sample_idx}, skipping"
            )
            continue
        processed_task_ids.add(sample["task_id"])
        if sample["task_id"] not in tasks_data:
            typer.echo(
                f"⚠️ Task ID '{sample['task_id']}' not found for sample {sample_idx}, skipping"
            )
            continue
        result: SampleResult = benchmark_config["evaluate"](
            tasks_data[sample["task_id"]], sample
        )
        results.append(result)

    # TODO: Print results to console

    # TODO: By default, output results to path/results as specified by README (or output-dir if specified)
    # Alias is from tasks.jsonl and should match the folder name
