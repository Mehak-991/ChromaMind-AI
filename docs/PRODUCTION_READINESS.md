# Production Readiness & Security Checklist

This document defines the validation criteria required before deploying ChromaMind AI to production environments.

---

## 1. Security Checklist
- [ ] **Secrets Management**: No API keys (Gemini, database credentials) are hardcoded. Ensure all environments read from AWS Secrets Manager or HashiCorp Vault.
- [ ] **CORS Settings**: Restrict `allow_origins` in `app/main.py` from `*` to specific production domains.
- [ ] **Rate Limiting**: Verify rate-limiting is active in Redis (limiting clients to 60 calls/minute).
- [ ] **JWT Key Rotation**: Implement JWT signature key expiration and token rotation.

---

## 2. Performance & Scaling Checklist
- [ ] **Engine Latency**: Verify average ML inference is under 5ms, and DE optimizer solver terminates in under 250ms.
- [ ] **Asynchronous Workers**: Confirm heavy search requests run in background Celery workers and do not block the Uvicorn web loop.
- [ ] **pgvector Indexing**: Ensure HNSW indexes are enabled on database vector search columns.

---

## 3. Monitoring & Diagnostics Checklist
- [ ] **Health Probes**: Expose `/health` and `/metrics` paths on FastAPI to Prometheus scraping.
- [ ] **Structured Logging**: Confirm `structlog` or `loguru` outputs JSON logs to stdout for Datadog or ELK Stack ingestion.
- [ ] **Model Drift Tracking**: Setup monitoring on model outputs to detect changes in raw material properties or base pigment updates.
