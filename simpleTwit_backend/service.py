from flask import Flask, render_template
from flask_cors import CORS
from flask_login import LoginManager

from model import db, User
import api

app = Flask(__name__, template_folder='frontend_assets', static_folder='frontend_assets', static_url_path='/')
CORS(app, supports_credentials=True)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = '20082003'
db.init_app(app)
api.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
