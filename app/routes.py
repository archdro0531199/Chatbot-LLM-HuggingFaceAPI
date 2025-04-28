from flask import Blueprint, render_template, request, session, redirect
from .chatbot import llm
import requests

main = Blueprint("main", __name__, template_folder="templates")

@main.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if "chat_history" not in session:
        session["chat_history"] = []
        
    if request.method == "POST":
        if "clear_chat" in request.form:
            session["chat_history"] = []
            session.modified = True
            return redirect("/")
        user_input = request.form.get("user_input")
        if user_input:
            response = llm(user_input, history=session["chat_history"])
            session["chat_history"].append({"role": "user", "text": user_input})
            session["chat_history"].append({"role": "bot", "text": response})
            session.modified = True
            
    return render_template("index.html", response=response, chat_history=session["chat_history"])

@main.route('/admin')
def admin_dashboard():
    # Hugging Face API Token
    hf_token = "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"
    
    headers = {
        "Authorization": f"Bearer {hf_token}"
    }
    response = requests.get("https://api-inference.huggingface.co/dashboard/billing/inference", headers=headers)

    if response.status_code == 200:
        data = response.json()
        used_amount = data.get("used", 0.0)
        total_quota = data.get("included", 0.0)
        remaining_quota = total_quota - used_amount
    else:
        used_amount = total_quota = remaining_quota = "無法取得資料"

    return render_template(
        "admin.html",
        used_amount=used_amount,
        total_quota=total_quota,
        remaining_quota=remaining_quota
    )