
export FLASK_APP=app/app.py

run:
	flask run --host=0.0.0.0

release:
	zip -r HAMA12128907_SALS20029908.zip . -x .\* app/__pycache__/\* app/.venv/\*

.PHONY: run release
