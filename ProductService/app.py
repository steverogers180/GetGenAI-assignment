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
            return jsonify({'message': 'Access denied'}), 401

        data = request.json
        title = data.get('title')
        content = data.get('content')
        status = data.get('status')

        session = Session()
        product = Product(title=title, content=content, status=status)
        session.add(product)
        session.commit()
        session.close()
        return jsonify({'message': 'Product added successfully', id: product.id })
    except Exception as e:
        print(e)
        return jsonify({'message': 'Could not add product'}), 500

@app.route('/product/list', methods=['GET'])
def list_products():
    try:
        is_valid_token, username = verify_token()
        if not is_valid_token:
            return jsonify({'message': 'Access denied'}), 401

        session = Session()
        products = session.query(Product).all()
        session.close()

        product_list = [{'id': product.id, 'title': product.title, 'content': product.content, 'status': product.status} for product in products]
        return jsonify(product_list)
    except Exception as e:
        print(e)
        return jsonify({'message': 'Could not list products'}), 500

@app.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    try:
        is_valid_token, username = verify_token()
        if not is_valid_token:
            return jsonify({'message': 'Access denied'}), 401

        session = Session()
        product = session.query(Product).filter_by(id=id).first()
        session.close()

        if product:
            return jsonify({'id': product.id, 'title': product.title, 'content': product.content, 'status': product.status})
        else:
            return jsonify({'message': 'Product not found'}), 404
    except Exception as e:
        print(e)
        return jsonify({'message': 'Could not get product'}), 500

@app.route('/product/update/<int:id>', methods=['PUT'])
def update_product(id):
    try:
        is_valid_token, username = verify_token()
        if not is_valid_token:
            return jsonify({'message': 'Access denied'}), 401

        session = Session()
        product = session.query(Product).filter_by(id=id).first()

        if not product:
            session.close()
            return jsonify({'message': 'Product not found'}), 404

        data = request.json
        product.title = data.get('title', product.title)
        product.content = data.get('content', product.content)
        product.status = data.get('status', product.status)

        session.commit()
        session.close()

        return jsonify({'message': 'Product updated successfully'})
    except Exception as e:
        print(e)
        return jsonify({'message': 'Could not update product'}), 500

@app.route('/product/delete/<int:id>', methods=['DELETE'])
def delete_product(id):
    try:
        is_valid_token, username = verify_token()
        if not is_valid_token:
            return jsonify({'message': 'Access denied'}), 401

        session = Session()
        product = session.query(Product).filter_by(id=id).first()

        if not product:
            session.close()
            return jsonify({'message': 'Product not found'}), 404

        session.delete(product)
        session.commit()
        session.close()

        return jsonify({'message': 'Product deleted successfully'})
    except Exception as e:
        print(e)
        return jsonify({'message': 'Could not delete product'}), 500

if __name__ == '__main__':
    port = 8000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    app.run(debug=True, port=port)
