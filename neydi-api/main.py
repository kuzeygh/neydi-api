from functools import wraps
from flask import Flask, jsonify, request
from firebase import operations

import uuid
import rsa

app = Flask(__name__)


def _token_check(token, signature):
    if token == 'vt':
        return True
    else:
        return False


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('token')
        if token is None:
            return jsonify({'message': 'there needs to be a token in headers but there is not.'})
        signature = request.headers.get('signature')
        if signature is None:
            return jsonify({'message': 'there needs to be a signature in headers but there is not.'})

        is_valid = _token_check(token, signature)
        if is_valid:
            return f(*args, **kwargs)
        else:
            return jsonify({'message': 'your token is not a valid token. sorry.'})
    return decorated_function


@app.route('/api/query', methods=['GET'])
@token_required
def query():
    return jsonify({"status": 'ok'})


@app.route('/api/add', methods=['POST'])
@token_required
def add_query():
    return jsonify({'status': 'ok'})


@app.route('/api/new', methods=['POST'])
def new_user():
    user_val = None
    email = request.json['email']

    (public, private) = rsa.newkeys(512)
    token = uuid.uuid4()

    try:
        user_val = operations.get_user(email).val()
    except:
        pass

    if user_val == None:
        db_result = operations.new_user(token=token, email=email,
                                        public=public, private=private)
    else:
        user_key = list(user_val.keys())[0]
        db_result = operations.update_user(key=user_key, token=token, email=email,
                                           public=public, private=private)

    return jsonify({'token': token, 'private-key': str(private)})


if __name__ == '__main__':
    app.run(debug=True)
