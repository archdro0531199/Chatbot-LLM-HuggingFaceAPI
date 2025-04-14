from flask import Flask
from app.routes import main

def create_app():
    app = Flask(
        __name__,
        static_folder="app/static",       
        template_folder="app/templates"
    )
    app.secret_key = "my_very_secret_key" #Open session function
    app.register_blueprint(main)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

