from flask import request, jsonify, make_response
from models.User import UserModel
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
import datetime
import jwt
import uuid
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

    password = generate_password_hash('12345678', method='pbkdf2:sha256')

    try:
        user = UserModel.query.filter_by(email=auth.username).first()
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
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=120),
            }

    if check_password_hash(password, auth.password):
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify({'token': token})

    return make_response(
            {'error': 'Wrong credentials'},
            401
         )


def register_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    new_user = {
            "id": uuid.uuid4(),
            'name': data['name'],
            'email': data['email'],
            'password': hashed_password
            }
    new_user = UserModel(
                email=data['email'],
                password=data['password']
            )
    print(new_user.email)
    print(new_user.password)
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception:
        return make_response(
                {'error': 'Something has gone wrong'},
                401
             )
    return jsonify({'message': 'Registered successfuly'})
