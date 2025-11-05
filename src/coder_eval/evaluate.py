import json
import typer
from pathlib import Path
from datetime import datetime
from coder_eval.docker_utils import ensure_docker_image
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


def print_results(
    results: list[SampleResult],
    benchmark_name: str,
    model_name: str,
    total_tasks: int,
) -> None:
    """Print benchmark evaluation summary to console."""
    evaluated_tasks = len(results)
    total_passed = sum(1 for r in results if r.get("passed_any", False))
    evaluated_failed = evaluated_tasks - total_passed
    unevaluated_tasks = total_tasks - evaluated_tasks

    print("────────────────────────────────────────────")
    print(
        f"✅ Evaluated {evaluated_tasks}/{total_tasks} tasks on {benchmark_name} with model {model_name}"
    )

    if evaluated_tasks > 0:
        print(
            f"   • Passed any: {total_passed}/{evaluated_tasks} ({total_passed / evaluated_tasks:.1%})"
        )
        print(f"   • Failed all: {evaluated_failed}/{evaluated_tasks}")
    else:
        print("   • No evaluated samples found.")

    if unevaluated_tasks > 0:
        print(f"   • Skipped/missing tasks: {unevaluated_tasks}")

    print(
        f"   • Overall: {total_passed}/{total_tasks} ({total_passed / total_tasks:.1%})"
    )

    print("────────────────────────────────────────────")

    for r in results:
        task_id = r.get("task_id", "unknown")
        passed_any = r.get("passed_any", False)
        num_passed = r.get("num_passed", 0)
        num_failed = r.get("num_failed", 0)

        status_icon = "✅" if passed_any else "❌"
        print(
            f"{status_icon} {task_id:<15} | pass={num_passed:<2} fail={num_failed:<2}"
        )

    all_exec_times = [
        er.get("exec_time", 0.0)
        for r in results
        for er in r.get("results", [])
        if er.get("exec_time") is not None
    ]

    if all_exec_times:
        avg_time = sum(all_exec_times) / len(all_exec_times)
        max_time = max(all_exec_times)
        print("\n⏱️  Avg exec time: {:.2f}s (max {:.2f}s)".format(avg_time, max_time))

    print("────────────────────────────────────────────")


@app.callback(invoke_without_command=True)
def evaluate(
    path: str = typer.Option(..., help="Path to benchmark directory."),
    samples: str = typer.Option(..., help="Path to JSONL file with model samples."),
    output_dir: str = typer.Option(None, help="Path to results directory."),
):
    """Evaluate generated samples."""
    typer.echo(f"Evaluating {samples} on benchmark at {path}")

    # Ensure Docker image is built
    ensure_docker_image()

    # Read tasks.jsonl from path
    tasks_path: Path = Path(path) / "tasks.jsonl"
    tasks_data: dict[str, Task] = read_tasks(tasks_path)
    if not tasks_data:
        typer.echo(f"❌ No tasks found in {tasks_path}")
        raise typer.Exit(1)
    typer.echo(f"✅ Read {len(tasks_data)} tasks from {tasks_path}")

    # Get benchmark config
    benchmark_id: str = next(iter(tasks_data.values()))["benchmark"]
    benchmark_config: BenchmarkConfig = get_benchmark_or_exit(benchmark_id)
    benchmark_name: str = benchmark_config["name"]

    # Read samples.jsonl
    samples_path: Path = Path(samples)
    samples_data: list[Sample] = read_samples(samples_path)
    if not samples_data:
        typer.echo(f"❌ No samples found in {samples_path}")
        raise typer.Exit(1)
    model_name: str = samples_data[0]["model_name"]
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

    # Print results to console
    print_results(results, benchmark_name, model_name, total_tasks=len(tasks_data))

    # Write results to JSONL file
    results_dir: Path = create_results_dir(
        Path(path),
        (Path(output_dir) if output_dir else None),
        benchmark_name,
        model_name,
    )
    with (results_dir / "results.jsonl").open("w", encoding="utf-8") as f:
        for result in results:
            f.write(json.dumps(result) + "\n")
    typer.echo(f"✅ Wrote {len(results)} results to {results_dir / 'results.jsonl'}")
