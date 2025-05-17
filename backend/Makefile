.PHONY: up down build logs shell seed test

up:
	docker-compose up --build

down:
	docker-compose down -v

build:
	docker-compose build

logs:
	docker-compose logs -f

shell:
	docker-compose exec api /bin/bash

seed:
	docker-compose exec api python scripts/seed_db.py

test:
	pytest tests/
