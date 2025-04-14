from flask import Blueprint, render_template, request, session, redirect
from .chatbot import llm

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

