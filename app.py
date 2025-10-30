
from flask import Flask
from routes.main import main

app = Flask(__name__)
app.secret_key = "senha_segura"
app.register_blueprint(main)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
