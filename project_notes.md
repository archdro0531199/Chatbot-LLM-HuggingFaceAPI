# 🧠 Project Notes: LLM Chatbot Development Log

**Date:** 2025-04-24
**Author:** Teresa (on behalf of user)

---

## Overview

This document outlines the step-by-step progression of integrating a large language model (LLM) into a medical assistant chatbot, comparing multiple deployment approaches and analyzing the final decision to revert to Hugging Face API for production usage.

---

## Phase 1: Local Inference Setup

**Objective:**  
Deploy `open_llama_7b_v2` locally using `transformers` and `torch`, with Flask as the web framework.

**Actions Taken:**
- Installed required packages: `transformers`, `accelerate`, `torch`, `sentencepiece`, `blobfile`, and `tiktoken`.
- Used `AutoTokenizer` and `AutoModelForCausalLM` to load the model locally.
- Enabled 16-bit precision (`torch.float16`) and `device_map="auto"` for GPU acceleration on a 32GB system.
- Implemented prompt engineering with session-based multi-turn memory using Flask and `session`.

**Issues Encountered:**
- Model load time was long.
- GPU memory exceeded frequently.
- Flask backend timed out during `.generate()`.
- Some sessions resulted in empty or malformed responses.

---

## Phase 2: Google Colab Deployment

**Objective:**  
Test inference in Colab with access to a free GPU runtime.

**Actions Taken:**
- Migrated local code to Colab.
- Re-tested using the same prompt strategy and tokenization.

**Issues Encountered:**
- GPU usage quota exhausted quickly.
- Environment reset between sessions.
- Unstable during long generations.

---

## Phase 3: Hugging Face API Integration

**Objective:**  
Align project with real-world job expectations and provide a hosted, stable LLM backend.

**Actions Taken:**
- Integrated `requests.post()` to call Hugging Face Inference API.
- Tested models: `HuggingFaceH4/zephyr-7b-beta`, `openlm-research/open_llama_7b_v2`, and `mistralai/Mistral-7B-Instruct`.
- Added error handling for API limits and latency.
- Implemented multilingual prompt switching (Chinese / English) with role guidance.

**Decision Factors:**
- Hugging Face API offered more reliable inference.
- Model warming and server management were abstracted.
- Reduced memory load and improved runtime stability.
- Job alignment with expectations in smart assistant engineering roles.

---

## Final Outcome

The system now runs using Hugging Face Inference API with:
- Language-sensitive prompt formatting
- Multi-turn context memory
- API reliability safeguards

This workflow mirrors production-ready smart assistant architecture, suitable for showcasing in job applications and technical portfolios.
