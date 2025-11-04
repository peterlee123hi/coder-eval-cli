import tempfile
import subprocess
import os
import shutil
import time
from pathlib import Path
from coder_eval.types import ExecResult

DOCKER_IMAGE = "coder-eval-python"
DOCKERFILE_PATH = Path(__file__).parent / "docker" / "Dockerfile"


def ensure_docker_image() -> None:
    """Ensure the sandbox Docker image exists locally, building it if necessary."""
    try:
        # Check if image already exists
        subprocess.run(
            ["docker", "image", "inspect", DOCKER_IMAGE],
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"✅ Found existing Docker image '{DOCKER_IMAGE}'")
    except subprocess.CalledProcessError:
        print(f"🔨 Building Docker image '{DOCKER_IMAGE}'...")

        # Use the project root as the build context (3 levels up from coder_eval/docker/)
        build_context = DOCKERFILE_PATH.parent.parent.parent

        subprocess.run(
            [
                "docker",
                "build",
                "-t",
                DOCKER_IMAGE,
                "-f",
                str(DOCKERFILE_PATH),
                str(build_context),
            ],
            check=True,
        )

        print(f"✅ Successfully built '{DOCKER_IMAGE}'")


def run_script(script: str) -> ExecResult:
    """Run arbitrary Python code safely inside a Docker container."""
    temp_dir = tempfile.mkdtemp(prefix="coder_eval_")
    script_path = os.path.join(temp_dir, "main.py")

    # Write the script to a temporary file
    with open(script_path, "w") as f:
        f.write(script)

    cmd = [
        "docker",
        "run",
        "--rm",
        "--network",
        "none",
        "--memory",
        "256m",
        "--cpus",
        "0.5",
        "--security-opt",
        "no-new-privileges",
        "--cap-drop",
        "ALL",
        "-v",
        f"{temp_dir}:/workspace",
        "-w",
        "/workspace",
        DOCKER_IMAGE,
        "python",
        "main.py",
    ]

    start_time = time.time()

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        elapsed = time.time() - start_time

        result: ExecResult = {
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
            "returncode": proc.returncode,
            "exec_time": elapsed,
        }

    except subprocess.TimeoutExpired:
        result = ExecResult(
            stdout="",
            stderr="TimeoutExpired",
            returncode=-1,
            exec_time=10.0,
            error="timeout",
        )

    except Exception as e:
        result = ExecResult(
            stdout="",
            stderr=str(e),
            returncode=-1,
            exec_time=0.0,
            error="exception",
        )

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

    return result
