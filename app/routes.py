from flask import Blueprint, render_template, request
from .chatbot import get_response

main = Blueprint('main', __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if request.method == "POST":
        user_input = request.form["user_input"]
        response = get_response(user_input)
    return render_template("index.html", response=response)

