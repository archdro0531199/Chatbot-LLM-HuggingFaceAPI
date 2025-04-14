import requests
import re

url = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
token = "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"  # Replace with your Hugging Face token

def detect_language(text):
    if re.search(r'[\u4e00-\u9fff]', text):
        return 'zh'
    return 'en'
    
def llm(query, history = None):
    
    history = history or []
    
    lang = detect_language(query)
    
    if lang == 'zh':
        system_prompt = "你是一個樂於助人的聰明助手，請用中文準確地回答用戶的提問"
    else:
        system_prompt = "You are a helpful and smart assistant. You accurately provide answers to user queries."

    conversation = ""
    
    for turn in history:
        if turn["role"] == "user":
            conversation += f"<|start_header_id|user|end_header_id|>\n{turn['text']}<|eot_id|>"
        elif turn["role"] == "bot":
            conversation += f"<start_header_id|>assistant<|end_header_id|>\n{turn['text']}<|eot_id|>"
            
    conversation += f"<|start_header_id|>user<|end_header_id|>\n{query}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
    
    prompt = f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n{system_prompt}\n<|eot_id|>{conversation}"

    parameters = {
        "max_new_tokens": 300,
        "temperature": 0.01,
        "top_k": 50,
        "top_p": 0.95,
        "return_full_text": False
    }
    

    headers = {
      'Authorization': f'Bearer {token}',
      'Content-Type': 'application/json'
    }

    

    payload = {
      "inputs": prompt,
      "parameters": parameters
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        print("[DEBUG] 回傳內容：", data)

        if isinstance(data, list) and 'generated_text' in data[0]:
            return data[0]['generated_text'].strip()
        elif isinstance(data, dict) and 'error' in data:
            return f"[ERROR] API 回傳錯誤：{data['error']}"
        else:
            return "[ERROR] 無法解析 API 回傳格式"

    except Exception as e:
        return f"[ERROR] 發生例外錯誤：{str(e)}"



