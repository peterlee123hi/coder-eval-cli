# Coder Eval CLI

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Authors:** Peter Lee ([peterlee123hi@cs.ucla.edu](mailto:peterlee123hi@cs.ucla.edu)), Ying Li ([ying.li@ucla.edu](mailto:ying.li@ucla.edu))

## Overview

**Coder Eval CLI** is a CLI tool to assist with evaluating coding agents on software engineering benchmarks.

### Key Features
- Evaluate code generation models and agents directly from the terminal
- Integrates with standard SWE benchmarks (SWE-bench verified, HumanEval, MBPP, APPS, LiveCodeBench)
- Manage local test repositories and custom tasks
- Generates detailed logs and a `stats.html` summary

## Installation

[TODO: complete this section]

## Usage

[TODO: complete this section]

```bash
# Loads benchmark locally
coder-eval prepare --benchmark mbpp

# Evaluate generated output
coder-eval evaluate --benchmark mbpp --samples sample.jsonl
coder-eval evaluate --custom_tasks tasks.jsonl --samples sample.jsonl

# List tasks within benchmark
coder-eval list-tasks --benchmark mbpp

# Load tasks within benchmark locally
coder-eval prepare-tasks --benchmark mbpp --tasks=task-id-00

# Load custom benchmark locally
coder-eval prepare --benchmark swe-bench-verified --name swe-bench-easy
coder-eval prepare --repo https://github.com/test-user/pytorch-code.git --name pytorch-bench
```

## Custom Tasks

This tool supports custom local repositories and tasks to evaluate models or agents on specific codebases. Each task specifies a repository snapshot, target files or diffs, and test cases to verify correctness.

`tasks.jsonl`
```json
[
  {
    "id": "myrepo_bugfix_42",
    "repo_path": "./repos/myrepo",
    "base_commit": "9f8e7d6",
    "patch_file": "./patches/fix_div_zero.diff",
    "test_file": "tests/test_division.py",
    "description": "Fix division by zero error in divide() in src/utils/math.py."
  }
]
```

### Options

```bash
--benchmark      humaneval | mbpp | apps | swe-bench-verified | livecodebench
--repo           https://www.github.com/test-user/sample-repo.git
--dir            ./benchmarks
--name           mbpp-only-arithmetic
--tasks          task-id-00
--samples        samples.jsonl
--output-dir     ./results
--custom_tasks   tasks.jsonl
```

## Output

Each evaluation run produces:

```
/results/
  ├── logs/task-id-00/results.json
  └── stats.html
```

`stats.html` contains performance (test runtime) and correctness metrics (missing/correct/incorrect tasks).
