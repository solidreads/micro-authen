

req:
	pip freeze > requirements.txt


run:
	python3 main.py


black:
	black . --exclude venv
