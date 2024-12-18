from flask import request, jsonify
from functools import wraps
import jwt
from config import SECRET_KEY


def token_required(f):
    @wraps(f)
    def decorator(*args, **kargs):
        '''
        token = None
        if 'Authorization' in request.headers:
            auth = request.headers['Authorization'].split()
            if (auth[0] == "Bearer"):
                token = auth[1]

        if not token:
            return jsonify({'message': 'there is no token'})
        print(token)

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = {
                    'id': data['public_id']
                    }
            print('user from jwt:')
            print(current_user)
        except Exception as e:
            print('error')
            print(e)
            return jsonify({'message': 'token is invalid'})
        '''

        return f(*args, **kargs)
    return decorator
