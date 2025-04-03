# CHANGELOG

---

## Day 1 - Initialize Project & Git Environment

- [chore] Initialize GitHub repo with `.gitignore`, `LICENSE`
- [chore] Create project structure: `app/`, `templates/`
- [setup] Configure Git Portable with global user.name and user.email
- [infra] Setup repo cloning, alias/path for Portable Python
- [test] Validate Python & Git workflow in local environment

---

## Day 2 - UI + LLM API Integration

- [feat] Add `templates/index.html` with input form and response display
- [feat] Implement `run.py` to launch Flask application
- [feat] Add `llm()` function to integrate Hugging Face Zephyr model with prompt generation
- [fix] Resolve `ImportError: get_response` by replacing with `llm()` or wrapper
- [safe] Add error handling for API return format (dict/list edge cases)
- [test] Successfully start local server and interact via browser
