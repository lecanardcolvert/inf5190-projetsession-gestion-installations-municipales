export FLASK_APP=app/app.py

run:
	flask run --host=0.0.0.0

checkstyle:
	pycodestyle app/ --exclude=.git,.venv

release:
	zip -r HAMA12128907_SALS20029908.zip . -x .\*  app/.venv/\* \*/__pycache__/\* \*/\*.log

.PHONY: run release
