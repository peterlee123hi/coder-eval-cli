install:
	poetry install

lint:
	poetry run ruff check src

format:
	poetry run black src

test:
	poetry run pytest -v

fix:
	poetry run ruff check src --fix
	poetry run black src

typecheck:
	poetry run mypy src
