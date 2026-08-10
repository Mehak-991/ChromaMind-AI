# Database Architecture - PostgreSQL Schema

This document details the database schema, table structures, and relationships for the ChromaMind AI system. It uses **PostgreSQL 15+** with the **`pgvector`** extension for storing embeddings related to the RAG knowledge retrieval and user session logs.

---

## 1. Extensions Required
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector"; -- Used for storing semantic document chunk embeddings (e.g. 1536 dim)
```

---

## 2. Table Schemas & DDL

### 2.1 Users Table
Stores authentication details and profile meta.
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    role VARCHAR(50) DEFAULT 'user' CHECK (role IN ('user', 'admin', 'scientist')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

### 2.2 User Sessions Table
Handles active refresh tokens and sign-in metadata.
```sql
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    refresh_token VARCHAR(512) UNIQUE NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sessions_user_id ON user_sessions(user_id);
```

### 2.3 Predictions Table
Captures color input coordinates, target, base configurations, and final mixing ratios.
```sql
CREATE TABLE predictions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    target_hex VARCHAR(7) NOT NULL,
    target_lab_l DOUBLE PRECISION NOT NULL,
    target_lab_a DOUBLE PRECISION NOT NULL,
    target_lab_b DOUBLE PRECISION NOT NULL,
    base_colors_config JSONB NOT NULL,    -- Stores array of base colors selected [ {hex, lab, id, name} ]
    ml_predicted_ratios JSONB NOT NULL,   -- Array of ratio weights initially suggested by ML model
    optimized_ratios JSONB NOT NULL,      -- Array of ratio weights after DE Optimization
    delta_e DOUBLE PRECISION NOT NULL,     -- Final similarity metric
    confidence_score DOUBLE PRECISION NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_predictions_user_id ON predictions(user_id);
CREATE INDEX idx_predictions_created_at ON predictions(created_at);
```

### 2.4 User Settings Table
Stores system options on a per-user basis.
```sql
CREATE TABLE user_settings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    default_delta_e_threshold DOUBLE PRECISION DEFAULT 1.0,
    optimizer_max_iterations INTEGER DEFAULT 1000,
    enable_explainability BOOLEAN DEFAULT TRUE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### 2.5 AI Logs & Chat History Table
Stores user conversations with the RAG agent. Contains raw messages and semantic embedding of queries for fast search/caching.
```sql
CREATE TABLE ai_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    prediction_context_id UUID REFERENCES predictions(id) ON DELETE SET NULL,
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    query_embedding vector(384),          -- Stores query vector representation for duplicate/cache checking
    citations JSONB,                      -- List of retrieved document details [ {title, source, snippet} ]
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ai_logs_user_id ON ai_logs(user_id);
```

### 2.6 Feedback Table
Enables reinforcement learning by allowing users to rate and correct formulas.
```sql
CREATE TABLE feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    prediction_id UUID NOT NULL REFERENCES predictions(id) ON DELETE CASCADE,
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    user_comment TEXT,
    actual_measured_hex VARCHAR(7),      -- If user measures real mix with spectrophotometer
    actual_measured_lab JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_feedback_prediction_id ON feedback(prediction_id);
```

### 2.7 Analytics Table
High-level event aggregation for business dashboard reporting.
```sql
CREATE TABLE analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_type VARCHAR(100) NOT NULL,     -- e.g., 'formulate_trigger', 'rag_query', 'export_formula'
    metadata JSONB,                       -- Action-specific stats
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_analytics_event_type ON analytics(event_type);
```

---

## 3. Vector Knowledge Base Table (RAG Metadata)
Stores chunks of text with their high-dimensional vector representations.
```sql
CREATE TABLE rag_knowledge_base (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_title VARCHAR(255) NOT NULL,
    chunk_content TEXT NOT NULL,
    embedding vector(384) NOT NULL,       -- Matches SentenceTransformers all-MiniLM-L6-v2 embedding dimension
    source_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- HNSW Vector Index for fast approximate nearest neighbor search
CREATE INDEX idx_rag_embedding ON rag_knowledge_base USING hnsw (embedding vector_cosine_ops);
```
