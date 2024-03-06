import os
import sys
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
import jwt
load_dotenv()

app = Flask(__name__)

DATABASE_URL = os.getenv('DB_URL')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

Base.metadata.create_all(engine)

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        session = Session()
        user = User(username=username, password=password)
        session.add(user)
        session.commit()
        session.close()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        print(e)
        return jsonify({'message': 'Could not register user'}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        session = Session()
        user = session.query(User).filter_by(username=username, password=password).first()
        session.close()
        if user:
            token = generate_token(username)
            return jsonify({'message': 'Login successful', 'token': token})
        else:
            return jsonify({'message': 'Invalid username or password'}), 401
    except Exception as e:
        print(e)
        return jsonify({'message': 'Could not login'}), 500

def generate_token(username):
    payload = {
        'username': username
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
    return token

if __name__ == '__main__':
    port = 5002
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    app.run(debug=True, port=port)
