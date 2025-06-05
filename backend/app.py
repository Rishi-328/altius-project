from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
import jwt
from datetime import datetime, timedelta
from functools import wraps
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/altiusinter'
app.config['SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a strong secret in production

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
CORS(app)

users = mongo.db.users
# ...existing code...

posts = mongo.db.posts

@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    if not title or not description:
        return jsonify({'message': 'Title and description required'}), 400
    post_id = posts.insert_one({'title': title, 'description': description}).inserted_id
    return jsonify({'message': 'Post created', 'id': str(post_id)}), 201

@app.route('/posts', methods=['GET'])
def get_posts():
    all_posts = []
    for post in posts.find():
        all_posts.append({
            'id': str(post['_id']),
            'title': post['title'],
            'description': post['description']
        })
    return jsonify(all_posts), 200

@app.route('/posts/<post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    if not title or not description:
        return jsonify({'message': 'Title and description required'}), 400
    result = posts.update_one(
        {'_id': mongo.db.ObjectId(post_id)},
        {'$set': {'title': title, 'description': description}}
    )
    if result.matched_count == 0:
        return jsonify({'message': 'Post not found'}), 404
    return jsonify({'message': 'Post updated'}), 200

@app.route('/posts/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    result = posts.delete_one({'_id': mongo.db.ObjectId(post_id)})
    if result.deleted_count == 0:
        return jsonify({'message': 'Post not found'}), 404
    return jsonify({'message': 'Post deleted'}), 200

# ...existing code...

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