from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(20), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    if not data.get('title'):
        return jsonify({'message': 'Title is required'}), 400
    new_task = Task(title=data['title'], description=data.get('description'), status=data.get('status', 'pending'))
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task created'}), 201

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.json
    task = Task.query.get(id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    db.session.commit()
    return jsonify({'message': 'Task updated'})

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'})

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password_hash, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)
    return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
