# Contributing & Coding Standards

This document establishes the repository guidelines, style guides, testing conventions, and git strategies for ChromaMind AI team members.

---

## 1. Coding Standards

### 1.1 Python Standards (Backend & ML)
- **Style Guide**: Follow **PEP 8** strictly.
- **Formatter**: `black` with standard line length of 88 characters.
- **Linter**: `flake8` for syntax issues; `isort` for import organization.
- **Type Annotations**: Explicit Python type hinting is required on all function definitions, class methods, and routing contracts (Pydantic models).
- **Naming Conventions**:
  - Functions & Variables: `snake_case` (e.g., `calculate_delta_e()`)
  - Classes: `PascalCase` (e.g., `DifferentialEvolutionSolver`)
  - Modules & Packages: `snake_case`

### 1.2 TypeScript Standards (Frontend)
- **Style Guide**: Standard ESLint configurations matching React and Next.js guidelines.
- **Formatter**: `prettier` for style uniformity.
- **Types**: Interfaces must be used for public-facing object models. Avoid using `any`; enforce `unknown` or custom generic forms if typings are dynamic.
- **Naming Conventions**:
  - Components & Pages: `PascalCase` (e.g., `ColorRatioMeter.tsx`)
  - Hooks: CamelCase prefixed with `use` (e.g., `useColorFormulator.ts`)
  - Utilities & Helpers: `camelCase` (e.g., `hexToLab.ts`)

### 1.3 Database Naming (PostgreSQL)
- Table names must be pluralized, lowercased, using snake_case (e.g., `user_sessions`, `predictions`).
- Primary keys must be UUID format and named `id`.
- Foreign key references should match the singularized parent table name suffixed with `_id` (e.g., `user_id`).

---

## 2. Git & Release Strategy

### 2.1 Branching Model (GitFlow Simplified)
- **`main`**: Reflects the latest production-stable state. Direct commits are forbidden.
- **`develop`**: Integration branch for new features. All pull requests are merged here first.
- **`feature/*`**: Scoped branches for developers working on tasks (e.g., `feature/add-shap-plots`).
- **`bugfix/*`**: Scoped branches targeting issues in staging (e.g., `bugfix/fix-rgb-boundaries`).

### 2.2 Commit Message Convention
We adhere to the **Conventional Commits** format:
- `feat`: A new feature (e.g., `feat(ml): integrate differential evolution optimizer`)
- `fix`: A bug fix (e.g., `fix(api): handle zero-division in delta_e`)
- `docs`: Documentation changes (e.g., `docs(readme): update environment setup details`)
- `chore`: Internal tool adjustments or dependency upgrades.

---

## 3. Testing Architecture & Strategy

To ensure production stability, we implement multi-layer testing:

### 3.1 Unit Testing
- **Backend (Python)**: Managed with `pytest`. Mock all database database calls using SQLAlchemy's transactional rollback setups.
- **Frontend (TS/React)**: Managed with `Vitest` and `React Testing Library`. Mock API connections.
- **ML Engine**: Test mathematical properties:
  - CIELAB transformations: Verify RGB $\rightarrow$ LAB $\rightarrow$ RGB returns original color codes within margin.
  - DE Constraints: Assert that optimized weights output sum up to $1.0$.

### 3.2 Integration & E2E Testing
- **APIs**: Execute integration tests using FastAPI's `TestClient` to verify auth flows, predictions, and history retrievals.
- **E2E (Playwright)**: Simulate full browser workflows (selecting base colors, adjusting target color picker, verifying ratios and SHAP chart renders).
