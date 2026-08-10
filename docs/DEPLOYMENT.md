# Deployment & CI/CD Architecture

This document defines the deployment setups, Docker orchestrations, environment configurations, and Git workflow strategies for ChromaMind AI.

---

## 1. Local Orchestration (`docker-compose.yml`)

The following config spins up the database, API server, background worker, Redis broker, and frontend client.

```yaml
version: '3.8'

services:
  postgres:
    image: pgvector/pgvector:pg15
    environment:
      POSTGRES_DB: chromamind_db
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: SecretPassword123
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin -d chromamind_db"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./apps/backend
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=postgresql://admin:SecretPassword123@postgres:5432/chromamind_db
      - REDIS_URL=redis://redis:6379/0
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - JWT_SECRET=${JWT_SECRET}
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy

  celery_worker:
    build:
      context: ./apps/backend
      dockerfile: Dockerfile
    command: celery -A app.core.celery worker --loglevel=info
    environment:
      - DATABASE_URL=postgresql://admin:SecretPassword123@postgres:5432/chromamind_db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
      - postgres

  frontend:
    build:
      context: ./apps/frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
    depends_on:
      - backend

volumes:
  pgdata:
```

---

## 2. CI/CD Architecture (GitHub Actions Pipelines)

We maintain three decoupled pipelines in `.github/workflows/` for continuous verification and deployment.

### 2.1 Backend CI Pipeline (`backend-ci.yml`)
Runs linting, formatting, security checks, and unit/integration tests on every Pull Request targetting `main` or `develop`.

```yaml
name: Backend CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd apps/backend
          pip install -r requirements.txt
          pip install pytest flake8 black
      - name: Run Black formatter check
        run: black --check app/
      - name: Run Flake8 linter
        run: flake8 app/
      - name: Run Pytest suite
        run: pytest tests/
```

### 2.2 CD Deployment Pipeline (`cd-deploy.yml`)
Builds production Docker images, uploads them to AWS ECR, and updates deployment manifests in AWS ECS/Kubernetes.

```yaml
name: Continuous Deployment

on:
  push:
    tags:
      - 'v*.*.*'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1
      - name: Build and Push Backend Image
        run: |
          docker build -t ${{ steps.login-ecr.outputs.registry }}/chromamind-backend:${{ github.ref_name }} ./apps/backend
          docker push ${{ steps.login-ecr.outputs.registry }}/chromamind-backend:${{ github.ref_name }}
      - name: Trigger ECS Fargate Task Update
        run: |
          aws ecs update-service --cluster chromamind-production --service backend-service --force-new-deployment
```

---

## 3. Environment Config Matrix (.env)

We require the following keys set in production environments:
```ini
# System Configuration
NODE_ENV=production
JWT_SECRET=super_secret_jwt_sign_key_902183

# Connections
DATABASE_URL=postgresql://db_user:secure_pwd@production-rds.cluster-1234.us-east-1.rds.amazonaws.com:5432/chromamind_prod
REDIS_URL=redis://production-cache.elasticache.us-east-1.amazonaws.com:6379/0

# LLM Providers
GEMINI_API_KEY=AIzaSyD_ExampleKey12345

# S3 Buckets (Model Storage & RAG Assets)
AWS_STORAGE_BUCKET_NAME=chromamind-prod-assets
AWS_DEFAULT_REGION=us-east-1
```
