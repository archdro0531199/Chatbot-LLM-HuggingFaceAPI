# app/chatbot.py
import re
import requests
#import torch
#from transformers import AutoTokenizer, AutoModelForCausalLM
from datetime import datetime

# Hugging Face API 設定
url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
token = "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" 

'''model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)'''

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
            "你是一位專業的醫療領域智慧助手，熟悉常見疾病、生理機能、健康促進與臨床流程，"
            "請以清楚、簡潔、具臨床專業的方式用中文回答提問。"
            "若你無法確定問題的答案，請回應「我建議您諮詢專業醫師」以避免錯誤資訊。"
            "請使用不超過3句話，簡明扼要回答。\n"
        )
    else:
        system_prompt = (
            "You are a professional medical assistant AI. You are familiar with common diseases, physiology, healthcare protocols, "
            "and hospital workflows. Please answer clearly, concisely, and in a clinically accurate manner in English. "
            "If unsure about the answer, say: 'I recommend consulting a healthcare professional.'"
            "Please answer briefly and concisely using no more than 3 sentences.\n"
        )

    prompt = f"{system_prompt}\n{history_text}User: {user_input}\nAssistant:\n"
    return prompt

def llm(user_input, history=None):
    history = (history or [])[-3:]
    prompt = build_prompt(user_input, history)
    
    # 設定 Hugging Face API headers
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 設定請求 payload
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.7,
            "top_k": 50,
            "top_p": 0.9,
            "return_full_text": False  # 只回傳回答，不回傳整個prompt
        }
    }

    try:
        print(f"[DEBUG] 發送請求：{datetime.now().strftime('%H:%M:%S')}")
        response = requests.post(url, headers=headers, json=payload)
        print(f"[DEBUG] 收到回應：{datetime.now().strftime('%H:%M:%S')}")

        data = response.json()
        print("[DEBUG] API 回傳內容：", data)

        # 正常回傳時，解析結果
        if isinstance(data, list) and "generated_text" in data[0]:
            answer = data[0]["generated_text"].strip()
            return answer if answer else "[助手無回應內容]"
        elif isinstance(data, dict) and "error" in data:
            return f"[ERROR] API錯誤：{data['error']}"
        else:
            return "[ERROR] 無法解析 API 回傳格式"

    except Exception as e:
        return f"[ERROR] 發生例外錯誤：{str(e)}"
    
    '''inputs = tokenizer(prompt, return_tensors="pt", padding=True).to(model.device)
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
        return "[⚠️ 無法識別模型回應格式]"'''
