import requests
import re

url = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
token = "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"  # Replace with your Hugging Face token

def detect_language(text):
    if re.search(r'[\u4e00-\u9fff]', text):
        return 'zh'
    return 'en'
    
def format_history(history):
    
    conversation = ""
    
    for turn in history:
        if turn["role"] == "user":
            conversation += f"<|start_header_id|user|end_header_id|>\n{turn['text']}<|eot_id|>"
        elif turn["role"] == "bot":
            conversation += f"<start_header_id|>assistant<|end_header_id|>\n{turn['text']}<|eot_id|>"
    return conversation
    
def build_prompt(user_input, history):
    lang = detect_language(user_input)
    history_text = format_history(history)
    
    if lang == 'zh':
        system_prompt = (
            "<|start_header_id|>system<|end_header_id|>\n"
            "你是一位專業的醫療領域智慧助手，熟悉常見疾病、生理機能、健康促進與臨床流程，"
            "請以清楚、簡潔、具臨床專業的方式用中文回答提問。"
            "若你無法確定問題的答案，請回應「我建議您諮詢專業醫師」以避免錯誤資訊。\n"
            "<|eot_id|>"
        )
    else:
        system_prompt = (
            "<|start_header_id|>system<|end_header_id|>\n"
            "You are a professional medical assistant AI. You are familiar with common diseases, physiology, healthcare protocols, "
            "and hospital workflows. Please answer clearly, concisely, and in a clinically accurate manner in English. "
            "If unsure about the answer, say: 'I recommend consulting a healthcare professional.'\n"
            "<|eot_id|>"
        )
    
    
    current_turn = f"<|start_header_id|>user<|end_header_id|>\n{user_input}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
    prompt = f"<|begin_of_text|>{system_prompt}{history_text}{current_turn}"
    return prompt

def llm(user_input, history = None):
    history = history or []
    prompt = build_prompt(user_input, history)


    headers = {
      'Authorization': f'Bearer {token}',
      'Content-Type': 'application/json'
    }

    
    payload = {
      "inputs": prompt,
      "parameters": {
          "max_new_tokens": 512,
          "temperature": 0.3,
          "top_k": 50,
          "top_p": 0.9,
          "return_full_text": False
      }
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



