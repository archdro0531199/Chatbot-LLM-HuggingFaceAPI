# app/chatbot.py
import re
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from datetime import datetime

model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)

def detect_language(text):
    if re.search(r'[\u4e00-\u9fff]', text):
        return 'zh'
    return 'en'

def format_history(history):
    conversation = ""
    for turn in history:
        if turn["role"] == "user":
            conversation += f"User: {turn['text']}\n"
        elif turn["role"] == "bot":
            conversation += f"Assistant: {turn['text']}\n"
    return conversation

def build_prompt(user_input, history):
    lang = detect_language(user_input)
    history_text = format_history(history)

    if lang == "zh":
        system_prompt = (
            "你是一位醫療智慧助手，請用清楚、簡潔、專業的中文回答問題。\n"
            "如果你不確定答案，請說「我建議您諮詢專業醫師」。\n"
        )
    else:
        system_prompt = (
            "You are a helpful medical assistant. Answer clearly and concisely in English. "
            "If unsure, respond with: 'I recommend consulting a healthcare professional.'\n"
        )

    prompt = f"{system_prompt}\n{history_text}User: {user_input}\nAssistant:"
    return prompt

def llm(user_input, history=None):
    history = (history or [])[-3:]
    prompt = build_prompt(user_input, history)

    inputs = tokenizer(prompt, return_tensors="pt", padding=True).to(model.device)
    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]

    with torch.no_grad():
        print(f"[DEBUG] 開始 generate()：{datetime.now().strftime('%H:%M:%S')}")
        output_ids = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_new_tokens=150,
            max_time=15,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id
        )
        print(f"[DEBUG] 結束 generate()：{datetime.now().strftime('%H:%M:%S')}")

    decoded = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    print(f"[DEBUG] 原始輸出：{decoded}")

    # 嘗試找最後一個 Assistant 回覆的位置
    if "Assistant:" in decoded:
        reply = decoded.split("Assistant:")[-1].strip()
        return reply if reply else "[助手無回應內容]"
    else:
        return "[⚠️ 無法識別模型回應格式]"
