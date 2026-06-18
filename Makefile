.PHONY: install install-dev test run

install:
	pip install .

install-dev:
	pip install ".[test]"

test:
	pytest tests

run:
	uvicorn src.main:app --reload

docker-build:
	docker build -t sammet-app:latest .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down