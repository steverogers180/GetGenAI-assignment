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

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    status = Column(String)

Base.metadata.create_all(engine)

def verify_token():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Authorization header missing'}), 401
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        if 'username' in payload:
            return True, payload['username']
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401
    return jsonify({'message': 'Unauthorized'}), 401

@app.route('/product/add', methods=['POST'])
def add_product():
    try:
        is_valid_token, username = verify_token()
        if not is_valid_token:
            return jsonify({'message': 'Access granted for user: ' + username})
        data = request.json
        title = data.get('title')
        content = data.get('content')
        status = data.get('status')
        session = Session()
        product = Product(title=title, content=content, status=status)
        session.add(product)
        session.commit()
        session.close()
        return jsonify({'message': 'Product added successfully'})
    except Exception as e:
        print(e)
        return jsonify({'message': 'Could not add product'}), 500

@app.route('/product/list', methods=['GET'])
def list_products():
    try:
        is_valid_token, username = verify_token()
        if not is_valid_token:
            return jsonify({'message': 'Access granted for user: ' + username})
        session = Session()
        products = session.query(Product).all()
        session.close()
        product_list = [{'id': product.id, 'title': product.title, 'content': product.content, 'status': product.status} for product in products]
        return jsonify(product_list)
    except Exception as e:
        print(e)
        return jsonify({'message': 'Could not list products'}), 500

if __name__ == '__main__':
    port = 8000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    app.run(debug=True, port=port)
