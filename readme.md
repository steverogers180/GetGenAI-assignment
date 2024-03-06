# Auth and Product Microservices

This repository contains two microservices: AuthService and ProductService. 

## AuthService

### Description
The AuthService is responsible for user authentication and token generation using JWT.

### How to Run

1. Make sure you have Docker installed on your system.
2. Clone this repository:

    ```bash
    git clone https://github.com/rahultrivedi180/GetGenAI-assignment.git
    ```

3. Navigate to the AuthService directory:

    ```bash
    cd AuthService
    ```

4. Build the Docker image:

    ```bash
    docker build -t auth-service .
    ```

5. Run the Docker container:

    ```bash
    docker run -d -p 5002:5002 auth-service
    ```

6. The AuthService should now be running on port 5002.

### Endpoints

- `POST /register`: Register a new user. Requires a JSON body with `username` and `password`.
- `POST /login`: Login with existing user credentials. Requires a JSON body with `username` and `password`.

## ProductService

### Description
The ProductService manages products, providing CRUD operations for products.

### How to Run

1. Make sure you have Docker installed on your system.
2. Clone this repository:

    ```bash
    git clone https://github.com/rahultrivedi180/GetGenAI-assignment.git
    ```

3. Navigate to the ProductService directory:

    ```bash
    cd ProductService
    ```

4. Build the Docker image:

    ```bash
    docker build -t product-service .
    ```

5. Run the Docker container:

    ```bash
    docker run -d -p 5001:5001 product-service
    ```

6. The ProductService should now be running on port 5001.

### Endpoints

- `POST /product/add`: Add a new product. Requires a JSON body with `title`, `content`, and `status`.
- `GET /product/list`: Get a list of all products.
- `GET /product/<id>`: Get details of a specific product by ID.
- `PUT /product/update/<id>`: Update details of a specific product by ID. Requires a JSON body with `title`, `content`, and `status`.
- `DELETE /product/delete/<id>`: Delete a product by ID.

### cURL Requests for Testing:

1. Register a new user:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"username": "example_user", "password": "example_password"}' http://localhost:5002/register
    ```

2. Login with existing user credentials:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"username": "example_user", "password": "example_password"}' http://localhost:5002/login
    ```

3. Add a new product:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"title": "New Product", "content": "Product description", "status": "active"}' http://localhost:5001/product/add
    ```

4. Get a list of all products:
    ```bash
    curl http://localhost:5001/product/list
    ```

5. Get details of a specific product by ID:
    ```bash
    curl http://localhost:5001/product/<product_id>
    ```

6. Update details of a specific product by ID:
    ```bash
    curl -X PUT -H "Content-Type: application/json" -d '{"title": "Updated Product", "content": "Updated description", "status": "inactive"}' http://localhost:5001/product/update/<product_id>
    ```

7. Delete a product by ID:
    ```bash
    curl -X DELETE http://localhost:5001/product/delete/<product_id>
    ```