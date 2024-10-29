default: lint type_check test

alias t := test

@test:
    uv run pytest tests/
    uv run coverage report --fail-under=100

alias tc := type_check

@type_check:
    uv run mypy src/ tests/

alias l := lint

@lint:
    uv run ruff format .
    uv run ruff check . --fix
