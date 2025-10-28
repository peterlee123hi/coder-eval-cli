from pathlib import Path
from coder_eval.evaluate import create_results_dir
import re


def test_create_results_dir_default(tmp_path: Path) -> None:
    """It should default to <path>/results/[timestamp]_<name>/"""
    bench_path: Path = tmp_path / "benchmarks" / "custom-bench"
    bench_path.mkdir(parents=True)

    outdir: Path = create_results_dir(bench_path, None, "custom-bench")

    assert outdir.exists()
    assert outdir.parent == bench_path / "results"
    assert re.match(r"\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}_custom-bench", outdir.name)


def test_create_results_dir_override(tmp_path: Path) -> None:
    """It should respect user-supplied output_dir and not add 'results/' nesting."""
    output_root: Path = tmp_path / "custom_results"
    output_root.mkdir(parents=True)

    outdir: Path = create_results_dir(Path("/any/path"), output_root, "mybench")

    assert outdir.exists()
    assert outdir.parent == output_root
    assert "mybench" in outdir.name
    assert re.match(r"\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}_mybench", outdir.name)
