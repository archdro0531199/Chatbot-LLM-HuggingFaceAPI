from flask import Blueprint, render_template, request, session
from .chatbot import get_response

main = Blueprint('main', __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if "chat_history" not in session:
        session["chat_history"] = []
    if request.method == "POST":
        user_input = request.form["user_input"]
        response = get_response(user_input)
        if user_input:
            session["chat_history"].append({"role": "user", "text": user_input})
            session["chat_history"].append({"role": "bot", "text": response})
            session.modified = True
    return render_template("index.html", response=response, chat_history=session["chat_history"])

