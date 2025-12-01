PY=uv run python manage.py

run:
	$(PY) runserver

migrate:
	$(PY) migrate

createsuperuser:
	$(PY) createsuperuser