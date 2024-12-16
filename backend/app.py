from flask import Flask
from routes import user_bp, chat_bp
from database import db

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)

app.register_blueprint(user_bp.user_bp)
app.register_blueprint(chat_bp.chat_bp)


if __name__ == "__main__":
    app.run(port=5000, host='localhost', debug=True)
