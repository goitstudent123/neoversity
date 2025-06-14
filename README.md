# Master of Science: Artificial Intelligence and Machine Learning

## Installation

Install the package
```shell
pip install .
```

Install pre-commit hook
```shell
pip install pre-commit && pre-commit install
```

## Format & Lint
Fix format
```shell
ruff check . --fix
```

Quality control
```shell
mypy tier1 tests
```

## Testing
Install development dependencies

```shell
pip install ".[dev]"
```

Run tests
```shell
PYTHONPATH=. pytest 
```

## Tier 1
