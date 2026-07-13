# Settings Centralization and Router Tests

## 1. Why this update matters

Projects that look like "vibe coding" often show the same patterns:

- configuration is scattered across many files
- environment variables are read ad hoc in each function
- UI or route responses are hard-coded in long inline blocks
- tests cover only fragments of utility logic

This update was meant to reduce those signals in Ops Monitor.

## 2. What changed

### 2.1 Shared settings module

A dedicated `app/config.py` module was added.

It now handles:

- `.env` loading
- boolean parsing
- host list parsing
- monitor interval and threshold loading
- log directory loading

Benefits:

- environment-dependent values are loaded in one place
- repeated `load_dotenv()` and `os.getenv()` calls are removed from service code
- configuration behavior becomes easier to test

### 2.2 Dashboard cleanup

The dashboard route was refactored to make the file easier to read and review.

Improvements:

- broken text was removed
- dashboard HTML is stored as a named constant
- route handlers now have explicit return types

This makes the route file look more intentional and less like temporary demo code.

### 2.3 Router and settings tests

New tests were added for:

- settings parsing
- settings cache reset behavior
- dashboard HTML rendering
- alert and monitoring status route responses

This matters because reviewers can see that the project is not only "working once" but also being checked at a unit level.

## 3. Practical lesson

Even in a small FastAPI project, moving configuration into one module and adding route-level tests improves:

- maintainability
- reviewability
- change safety
- portfolio credibility

The goal is not just to make the app run, but to make the code explain itself when someone else reads it.
