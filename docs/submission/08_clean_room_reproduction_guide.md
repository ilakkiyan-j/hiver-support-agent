# 08 — Clean-Room Reproduction & Quick-Start Guide

---

## 1. Prerequisites

* **Python**: Version 3.10+
* **Dependencies**: Installed via `requirements.txt`
  ```bash
  pip install -r requirements.txt
  ```

---

## 2. Environment Configuration

Copy `.env.example` to `.env` and add your Gemini API key:
```bash
cp .env.example .env
```

Ensure `.env` contains:
```env
LLM_PROVIDER=google
LLM_MODEL=gemini-2.5-flash
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## 3. Run Automated Unit & Integration Tests

Run the complete 21-test suite:
```bash
pytest -v
```

---

## 4. Run One-Command Clean-Room Reproduction

Execute the master reproduction script to run data loading, baseline evaluation, agent evaluation, and failure analysis:
```bash
python scripts/reproduce_all.py
```

*Expected output*: Prints execution metrics summary table in terminal and saves JSON report to `data/reproduction_summary.json` in under 40 seconds.

---

## 5. Launch Interactive Web UI & API Server

Start the server:
```bash
uvicorn src.api.main:app --reload --port 8000
```

* **Web UI Dashboard**: `http://localhost:8000`
* **Swagger API Docs**: `http://localhost:8000/docs`
