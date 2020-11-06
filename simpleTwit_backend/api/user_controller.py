import bcrypt
from flask import Blueprint, request, jsonify
from flask_login import logout_user, login_user, current_user, login_required
from model import db, User

app = Blueprint('{}_api'.format(__name__), __name__, url_prefix='/api/user')


def add_user(username, email, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = User(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return user


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        add_user(username=request.json['name'], email=request.json['email'], password=request.json['password'])
        return "Success"

    users = User.query.all()

    def map_user(user):
        return user.to_dict()

    users = map(map_user, users)
    users = list(users)
    return jsonify(users=users)


@app.route("/login", methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    user = User.query.filter_by(email=email).first()
    if user:
        if bcrypt.checkpw(password=password.encode('utf-8'), hashed_password=user.password):
            login_user(user)
            return user.username

    return 'please login again!'


@app.route('/checklogin', methods=['GET'])
def check_login():
    user = current_user.is_authenticated
    if not user:
        return "Fail"
    else:
        return jsonify(status='success', username=current_user.username)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return 'logged out!'
