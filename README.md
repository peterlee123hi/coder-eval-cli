# Coder Eval CLI

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Authors:** Peter Lee ([peterlee123hi@cs.ucla.edu](mailto:peterlee123hi@cs.ucla.edu)), Ying Li ([ying.li@ucla.edu](mailto:ying.li@ucla.edu))

**Coder Eval CLI** is a tool to assist with evaluating LLMs on coding benchmarks.

### Key Features
- Prepare benchmarks locally for code generation models
- Integrates with standard coding benchmarks including HumanEval and MBPP
- Generates detailed logs and evaluation summary

## Installation

[TODO: complete this section]

## Usage

[TODO: complete this section]

```bash
# Loads benchmark locally
coder-eval prepare --benchmark mbpp --path ./benchmarks/custom-mbpp

# Evaluate generated output
coder-eval evaluate --path ./benchmarks/custom-mbpp --samples sample.jsonl
```

### Options

```bash
--benchmark      humaneval | mbpp
--path           ./benchmarks/custom-bench
--samples        samples.jsonl
--output-dir     ./benchmarks/custom-bench/results
```

## Supported Benchmarks

| Benchmark | Dataset Source | Description | Revision |
|------------|----------------|--------------|---------------|
| **HumanEval** | [openai/openai_humaneval](https://huggingface.co/datasets/evalplus/humanevalplus) | 164 short Python function synthesis tasks. | `7dce605` |
| **MBPP** | [Muennighoff/mbpp](https://huggingface.co/datasets/evalplus/mbppplus) | 500 mostly beginner Python programming problems. | `d81b829` |

## Samples Format

The `samples.jsonl` file should contain the results to evaluate and have a list of generated completions for each task.

```json
{
  "task_id": 42,
  "model_name": "gpt-4",
  "completions": ["def add(a, b): return a + b"],
}
```

## Task Metadata

The `tasks.jsonl` metadata file is used to specify tasks in the benchmark to evaluate (e.g. `./benchmarks/custom-benchmark/tasks.jsonl`).

```json
{
  "task_id": "mbpp_001",
  "benchmark": "mbpp",
  "prompt": "Write a Python function to compute factorial of a number.",
  "entry_point": "factorial",
  "reference_solution": "def factorial(n): ...",
  "tests": ["assert factorial(5) == 120"],
}
```

## Output

Each evaluation run produces:

```
/benchmarks/custom-bench/results/
  └── [timestamp]_[benchmark]/
        └── results.jsonl                          # detailed per completion logs
```
