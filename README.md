# Coder Eval CLI

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Authors:** Peter Lee ([peterlee123hi@cs.ucla.edu](mailto:peterlee123hi@cs.ucla.edu)), Ying Li ([ying.li@ucla.edu](mailto:ying.li@ucla.edu))

## Overview

**Coder Eval CLI** is a tool to assist with testing LLMs on coding benchmarks.

### Key Features
- Prepare local datasets for code generation models
- Integrates with standard coding benchmarks including HumanEval, MBPP, APPS
- Generates detailed logs and evaluation summary

## Installation

[TODO: complete this section]

## Usage

[TODO: complete this section]

```bash
# Loads benchmark locally
coder-eval prepare --benchmark mbpp --path ./benchmarks/mbpp
coder-eval prepare --benchmark mbpp --tasks 4 --path ./benchmarks/mbpp-task4

# Evaluate generated output
coder-eval evaluate --path ./benchmarks/mbpp-easy-only --samples sample.jsonl
coder-eval evaluate --path ./benchmarks/mbpp-task4 --samples sample.jsonl

# List tasks within benchmark
coder-eval list-tasks --benchmark mbpp
coder-eval list-tasks --benchmark mbpp --page-size 20
```

### Options

```bash
--benchmark      humaneval | mbpp | apps
--path           ./benchmarks/custom-bench
--tasks          task-id-00
--samples        samples.jsonl
--output-dir     ./benchmarks/custom-bench/results
```

## Sample Format

The results to evaluate (`--samples`) must be a `.jsonl` file of generated completions:

```
{"task_id": 42, "completion": "def add(a, b): return a + b"}
```

## Task Metadata

The `tasks.jsonl` metadata file is used to specify tasks in the benchmark to evaluate (e.g. `./benchmarks/custom-benchmark/tasks.jsonl`).

```json
[
  {
    "task_id": "mbpp_001",
    "benchmark": "mbpp",
    "prompt": "Write a Python function to compute factorial of a number.",
    "entry_file": "main.py",
    "test_file": "test_main.py",
    "reference_solution": "def factorial(n): ...",
    "tests": ["assert factorial(5) == 120"],
  },
]
```

## Output

Each evaluation run produces:

```
/benchmarks/custom-bench/results/
  └── [timestamp]_[benchmark]/
        ├── results.jsonl                          # per-task outcomes
        ├── stdout.log                             # console logs
        └── summary.json                           # aggregated metrics
```
