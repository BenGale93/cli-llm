default: lint type_check test

alias t := test

@test:
    COV_CORE_SOURCE=src COV_CORE_CONFIG=pyproject.toml COV_CORE_DATAFILE=.coverage.eager uv run pytest

alias tc := type_check

@type_check:
    uv run mypy src/ tests/

alias l := lint

@lint:
    uv run ruff format .
    uv run ruff check . --fix
