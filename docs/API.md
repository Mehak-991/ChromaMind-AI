# API Documentation - ChromaMind AI REST Specification

This document details the REST API specification for the ChromaMind AI platform backend (FastAPI). All endpoints are versioned under `/api/v1` and enforce standard JSON request and response payloads.

---

## 1. Global Headers and Conventions
- **Base URL**: `https://api.chromamind.ai/api/v1`
- **Content-Type**: `application/json`
- **Authorization**: `Bearer <JWT_TOKEN>` (for protected endpoints)

---

## 2. Authentication APIs

### 2.1 User Registration
- **Endpoint**: `POST /auth/register`
- **Access**: Public
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "StrongSecurePassword123!",
    "full_name": "John Doe"
  }
  ```
- **Response (201 Created)**:
  ```json
  {
    "id": "u_9f81a7b4-32cd-4ef5-9a4d-82d8c3e8e19c",
    "email": "user@example.com",
    "full_name": "John Doe",
    "created_at": "2026-08-07T02:13:45Z"
  }
  ```

### 2.2 User Login
- **Endpoint**: `POST /auth/login`
- **Access**: Public
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "StrongSecurePassword123!"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 3600
  }
  ```

---

## 3. Prediction & Formulation APIs

### 3.1 Run Color Formulation Pipeline
Triggers the Machine Learning ratio prediction followed by Differential Evolution optimization.
- **Endpoint**: `POST /formulator/predict`
- **Access**: Protected
- **Request Body**:
  ```json
  {
    "target_color": {
      "hex": "#3A86C8",
      "lab": { "L": 52.4, "a": -5.3, "b": -41.2 }
    },
    "base_colors": [
      { "id": "base_red", "hex": "#FF0000", "lab": { "L": 53.2, "a": 80.1, "b": 67.2 } },
      { "id": "base_blue", "hex": "#0000FF", "lab": { "L": 32.3, "a": 79.2, "b": -108.3 } },
      { "id": "base_white", "hex": "#FFFFFF", "lab": { "L": 100.0, "a": 0.0, "b": 0.0 } },
      { "id": "base_yellow", "hex": "#FFFF00", "lab": { "L": 97.1, "a": -16.0, "b": 94.3 } }
    ],
    "run_optimization": true
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "prediction_id": "p_8f6d7c8e-4a3b-2c1d-0e9f-8a7b6c5d4e3f",
    "target_color": { "hex": "#3A86C8", "lab": { "L": 52.4, "a": -5.3, "b": -41.2 } },
    "formulation": {
      "base_ratios": [
        { "id": "base_red", "ratio": 0.05, "weight_grams": 5.0 },
        { "id": "base_blue", "ratio": 0.45, "weight_grams": 45.0 },
        { "id": "base_white", "ratio": 0.40, "weight_grams": 40.0 },
        { "id": "base_yellow", "ratio": 0.10, "weight_grams": 10.0 }
      ],
      "ml_predicted_ratios": [0.07, 0.43, 0.38, 0.12],
      "delta_e": 0.42,
      "confidence_score": 0.947
    },
    "explanation": {
      "shap_values": {
        "base_red": 0.12,
        "base_blue": 0.48,
        "base_white": -0.21,
        "base_yellow": 0.05
      },
      "summary": "Blue is the primary driver to reach the targeted saturation, while White corrects lightness."
    }
  }
  ```

---

## 4. History and Settings APIs

### 4.1 Get Prediction History
- **Endpoint**: `GET /history`
- **Access**: Protected
- **Query Parameters**:
  - `page`: default `1`
  - `limit`: default `10`
- **Response (200 OK)**:
  ```json
  {
    "items": [
      {
        "prediction_id": "p_8f6d7c8e-4a3b-2c1d-0e9f-8a7b6c5d4e3f",
        "target_color": "#3A86C8",
        "delta_e": 0.42,
        "created_at": "2026-08-07T02:15:00Z"
      }
    ],
    "total": 120,
    "page": 1,
    "limit": 10
  }
  ```

### 4.2 Update Settings
- **Endpoint**: `PATCH /settings`
- **Access**: Protected
- **Request Body**:
  ```json
  {
    "default_delta_e_threshold": 1.0,
    "optimizer_max_iterations": 1000,
    "enable_explainability": true
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "status": "success",
    "updated_settings": {
      "default_delta_e_threshold": 1.0,
      "optimizer_max_iterations": 1000,
      "enable_explainability": true
    }
  }
  ```

---

## 5. RAG & AI Copilot APIs

### 5.1 Chat with AI Assistant
- **Endpoint**: `POST /rag/chat`
- **Access**: Protected
- **Request Body**:
  ```json
  {
    "message": "Why did the system recommend adding 10% white base color?",
    "prediction_context_id": "p_8f6d7c8e-4a3b-2c1d-0e9f-8a7b6c5d4e3f"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "response": "White base color has a high lightness L* of 100. The target color has a target L* of 52.4. Adding 40% white helps lift the mixture from the dark blue spectrum into the targeted medium-lightness sky blue.",
    "citations": [
      {
        "title": "Industrial Color Mixing Standards",
        "snippet": "To increase CIELAB lightness (L*), titanium dioxide white pigment is introduced...",
        "confidence": 0.98
      }
    ]
  }
  ```

---

## 6. Health & Diagnostics APIs

### 6.1 Liveness Probe
- **Endpoint**: `GET /health`
- **Access**: Public
- **Response (200 OK)**:
  ```json
  {
    "status": "healthy",
    "timestamp": "2026-08-07T02:13:32Z",
    "services": {
      "database": "connected",
      "redis": "connected",
      "ml_engine": "online"
    }
  }
  ```
