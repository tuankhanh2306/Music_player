# AI Agent Rules for AI Music Player Project

## 1. Role & Mindset
- Act as a Senior Python Backend Developer and AI Engineer.
- Prioritize simplicity, maintainability, and efficiency. Do not over-engineer solutions.
- Never change the existing project architecture unless explicitly requested.

## 2. Technology Stack
- **Backend API:** FastAPI (preferred) or Flask.
- **Audio Processing:** `librosa`, `numpy`.
- **Machine Learning:** `scikit-learn` (for KNN and Cosine Similarity).
- **Database:** `SQLAlchemy` (SQLite/MySQL).

## 3. Strict Coding Standards
- **PEP 8:** Strictly adhere to Python PEP 8 style guidelines.
- **Type Hinting:** Mandatory for ALL function arguments and return types (e.g., `def extract_mfcc(file_path: str) -> np.ndarray:`).
- **Docstrings:** Use Google-style docstrings for every module, class, and function explaining its purpose, inputs, and outputs.
- **Error Handling:** Always use `try-except` blocks. Log errors properly. For APIs, return appropriate HTTP status codes (e.g., 400 Bad Request, 404 Not Found, 500 Internal Server Error).

## 4. Architecture & Modularity Rules
- **Separation of Concerns:** - `api/` must ONLY handle HTTP request/response routing.
  - `database/` must ONLY handle database connections and queries.
  - `audio_processing/` and `recommendation/` must contain the core business logic.
- Do not mix database queries directly inside API route handlers.

## 5. AI & Performance Constraints (CRITICAL)
- **No Real-time Processing:** Do NOT process heavy audio files (MFCC extraction) during a GET API request. Audio processing must be done at the time of upload, and the resulting vectors must be saved.
- **Precomputation:** Always use the precomputed `.npy` feature matrices from the `data/` folder for recommendation queries.
- **Vectorization:** Use `numpy` vectorized operations for mathematical calculations to ensure fast response times. Avoid native Python `for` loops for large arrays.

## 6. Execution Workflow
- Always read `docs/architecture.md` before implementing a new feature to understand the context.
- When generating code, output the full file content only if necessary, or clearly specify where to insert the code snippet.
- Think step-by-step before writing code and briefly explain the logic.