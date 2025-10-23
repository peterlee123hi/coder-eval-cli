# Coder Eval CLI

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Authors:** Peter Lee ([peterlee123hi@cs.ucla.edu](mailto:peterlee123hi@cs.ucla.edu)), Ying Li ([ying.li@ucla.edu](mailto:ying.li@ucla.edu))

## Overview

**Coder Eval CLI** is a tool to assist with testing LLM coding agents on SWE benchmarks.

### Key Features
- Test code generation models and agents from the terminal
- Integrates with standard coding benchmarks including problem-based (HumanEval, MBPP, APPS) and repository-based (SWE-bench verified, LiveCodeBench)
- Manage local test repositories and custom tasks
- Generates detailed logs and a `stats.html` summary

## Installation

[TODO: complete this section]

## Usage

[TODO: complete this section]

```bash
# Loads benchmark locally
coder-eval prepare --benchmark mbpp --path ./benchmarks/mbpp
coder-eval prepare --benchmark swe-bench-verified --tasks 4 --path ./benchmarks/swe-bench-verified-task4
coder-eval prepare --repo https://github.com/test-user/pytorch-code.git --path ./benchmarks/pytorch-bench

# Evaluate generated output
coder-eval evaluate --path ./benchmarks/mbpp --samples sample.jsonl
coder-eval evaluate --path ./benchmarks/swe-bench-verified-task4 --samples sample.jsonl
coder-eval evaluate --path ./benchmarks/custom-bench --samples sample.jsonl

# List tasks within benchmark
coder-eval list-tasks --benchmark swe-bench-verified
```

### Options

```bash
--benchmark      humaneval | mbpp | apps | swe-bench-verified | livecodebench
--repo           https://www.github.com/test-user/sample-repo.git
--path           ./benchmarks/custom-bench
--tasks          task-id-00
--samples        samples.jsonl
--output-dir     ./results
```

## Sample Format

For problem-based benchmarks (MBPP, HumanEval, APPS), `--samples` must be a `.jsonl` file of generated completions:

```
{"task_id": 42, "completion": "def add(a, b): return a + b"}
```

For repository-based benchmarks (SWE-Bench, LiveCodeBench), `--samples` must be a `.jsonl` file or directory describing patches:

```
{"task_id": 4, "files": [{"path": "src/db.py", "patch": "@@ -22,7 +22,8 @@ ..."}]}
```

## Task Metadata

For problem-based and repository-based benchmarks, the `tasks.jsonl` metadata file is used to specify tasks in the benchmark to evaluate (e.g. `./benchmarks/custom-benchmark/tasks.jsonl`). Each task specifies a repository snapshot, target files or diffs, and test cases to verify correctness.

```json
[
  {
    "id": "mbpp_001",
    "type": "problem",
    "prompt": "Write a Python function to compute factorial of a number.",
    "entry_file": "main.py",
    "test_file": "test_main.py",
    "reference_solution": "def factorial(n): ...",
    "tests": ["assert factorial(5) == 120"],
    "description": "Basic recursion problem."
  },
  {
    "id": "myrepo_bugfix_42",
    "type": "repo",
    "repo_path": "./repos/myrepo",
    "base_commit": "9f8e7d6",
    "patch_file": "./patches/fix_div_zero.diff",
    "test_file": "tests/test_division.py",
    "description": "Fix division by zero error in divide()."
  }
]
```

## Output

Each evaluation run produces:

```
/results/
  └── [timestamp]_[benchmark]/
        ├── results.json                           # evaluation results
        └── stats.html                             # summary report
```

`stats.html` contains performance (test runtime) and correctness metrics (missing/correct/incorrect tasks).
