.PHONY: install lint test build up down clean

install:
	cd apps/frontend && npm install --legacy-peer-deps
	cd apps/backend && pip install -r requirements.txt
	cd packages/ml-engine && pip install -r requirements.txt
	cd packages/agent-engine && pip install -r requirements.txt

lint:
	cd apps/frontend && npm run lint
	black --check apps/backend packages/ml-engine packages/agent-engine
	ruff check apps/backend packages/ml-engine packages/agent-engine

test:
	cd apps/backend && pytest tests/
	cd packages/ml-engine && pytest tests/
	cd packages/agent-engine && pytest tests/

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
