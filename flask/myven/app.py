from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/altiusinter'
app.config['SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a strong secret in production

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
CORS(app)

users = mongo.db.users

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        if not token:
            return jsonify({'message': 'No token provided'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = users.find_one({'username': data['username']})
            if not current_user:
                raise Exception('User not found')
        except Exception:
            return jsonify({'message': 'Invalid token'}), 401
        return f(data['username'], *args, **kwargs)
    return decorated

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'Username and password required'}), 400
    if users.find_one({'username': username}):
        return jsonify({'message': 'Username already exists'}), 400
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    users.insert_one({'username': username, 'password': hashed_password})
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'Username and password required'}), 400
    user = users.find_one({'username': username})
    if not user or not bcrypt.check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid credentials'}), 401
    token = jwt.encode(
        {'username': username, 'exp': datetime.utcnow() + timedelta(hours=1)},
        app.config['SECRET_KEY'],
        algorithm="HS256"
    )
    return jsonify({'token': token})

@app.route('/profile', methods=['GET'])
@token_required
def profile(current_username):
    return jsonify({'message': f'Welcome, {current_username}'})

if __name__ == '__main__':
    app.run(port=5000, debug=True)