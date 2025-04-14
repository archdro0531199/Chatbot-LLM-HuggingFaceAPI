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

---

## Day 3
- refactor: 調整 Flask 專案結構，將 routes.py 拆分為 Blueprint 架構
- fix: 解決 TemplateNotFound 錯誤，手動指定 template_folder、static_folder
- debug: 測試 session 儲存對話紀錄功能

---

## Day 4
- feat: 實作捲軸對話區 UI（chat-log with overflow-y）
- fix: 解決 CSS 無法套用問題（static_folder 載入修正）
- test: 加入假對話測試捲軸效果

---

## Day 5
- feat: 整合 Hugging Face API 回傳，支援中英文對應語言回覆
- refactor: 將 prompt 語言切換邏輯統一封裝

---

## Day 6
- feat: 新增「清除對話」按鈕與處理邏輯
- style: 建立輸入欄與送出按鈕樣式架構（後續待補 UI 美化）
