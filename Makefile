# to run command: make <command>
# to run command with arg: make <command> arg="some_arg"

run:
	poetry run uvicorn app.main:app --reload

format:
	poetry run isort app
	poetry run black app

format_selected:
	poetry run isort $(path)
	poetry run black $(path)

lint:
	poetry run flake8 app

mypy:
	poetry run mypy app

lint_selected:
	poetry run flake8 $(path)

tests:
	poetry run pytest -vvv

migrations_create:
	poetry run alembic revision --autogenerate -m $(comment)

migrations_run:
	poetry run alembic upgrade head

migrations_downgrade:
	poetry run alembic downgrade head

coverage:
	poetry run coverage run -m pytest
	poetry run coverage report -m

worker:
	poetry run celery -A app.celery_loans.tasks worker --loglevel=INFO

beat:
	poetry run celery -A app.celery_loans.tasks beat --loglevel=INFO

flower:
	poetry run celery -A app.celery_loans.tasks flower
