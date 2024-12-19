from flask import request, jsonify, make_response
from models.User import UserModel
# from werkzeug.security import generate_password_hash, check_password_hash
from database import db
import datetime
import jwt
import uuid
import bcrypt
from config import SECRET_KEY


def getUser(user_id):
    user = UserModel.query.filter_by(id=user_id).first()
    return jsonify({
            'id': user.id,
            'email': user.email
        })


def login_user():

    print("hello")

    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response(
                {'error': 'Login required'},
                401
             )

    # password = generate_password_hash('12345678', method='pbkdf2:sha256')

    try:
        user = UserModel.query.filter_by(email=auth.username).first()
        print('my user')
        print(user.id)
        print(user.email)
        print(user.password)
    except Exception:
        return make_response(
                {'error': 'Wrong credentials'},
                401
             )

    payload = {
            'public_id': str(user.id),
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=2),
            }
    userPassword = auth.password.encode('utf-8')
    hashed_password = user.password.encode('utf-8')

    if bcrypt.checkpw(userPassword, hashed_password):
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify({
            'token': token,
            'userId': user.id
            })

    return make_response(
            {'error': 'Wrong credentials'},
            401
         )


def register_user():
    data = request.get_json()

    bytes = data['password'].encode('utf-8')

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(bytes, salt)
    string_password = hashed_password.decode('utf-8')

    # hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    new_user = UserModel(
                email=data['email'],
                password=string_password
            )

    print(new_user.email)
    print(new_user.password)
    print("len", len(new_user.password))
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        print("error")
        print(e)
        return make_response(
                {'error': 'Something has gone wrong'},
                401
             )
    payload = {
            'public_id': str(new_user.id),
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=2),
            }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return jsonify({
            'token': token,
            'userId': new_user.id
            })
