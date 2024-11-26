from flask import Flask, request, jsonify
import uuid
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  

# Mock data storage for users, orders, and payments
users = {"bakery_user": "password123"}  
orders = {}
payments = {}

# Helper function to create a JWT token
def create_token(username):
    payload = {
        "username": username,
        "exp": datetime.utcnow() + timedelta(hours=1)  
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")

# Middleware for token verification
def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing!"}), 401
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401
        return f(*args, **kwargs)
    return wrapper

# Root route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Bakery Payment Web Service"}), 200

# Login route to get a token
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if username in users and users[username] == password:
        token = create_token(username)
        return jsonify({"token": token}), 200

    return jsonify({"error": "Invalid credentials"}), 401

# Protected route to create a new order
@app.route('/create-order', methods=['POST'])
@token_required
def create_order():
    data = request.json
    if not data or not all(key in data for key in ("bakery_name", "items", "total_amount")):
        return jsonify({"error": "Invalid input data"}), 400

    order_id = str(uuid.uuid4())
    order = {
        "order_id": order_id,
        "bakery_name": data["bakery_name"],
        "items": data["items"],
        "total_amount": data["total_amount"],
        "status": "pending",
        "created_at": datetime.utcnow().isoformat()
    }
    orders[order_id] = order
    return jsonify({"message": "Order created", "order_id": order_id}), 200

# Protected route to initiate payment
@app.route('/initiate-payment', methods=['POST'])
@token_required
def initiate_payment():
    data = request.json
    if not data or "order_id" not in data:
        return jsonify({"error": "Order ID is required"}), 400

    order_id = data["order_id"]
    order = orders.get(order_id)

    if not order:
        return jsonify({"error": "Order not found"}), 404

    transaction_id = str(uuid.uuid4())
    payment = {
        "transaction_id": transaction_id,
        "order_id": order_id,
        "amount": order["total_amount"],
        "status": "success",
        "timestamp": datetime.utcnow().isoformat()
    }
    payments[transaction_id] = payment
    order["status"] = "paid"

    return jsonify({
        "message": "Payment initiated",
        "transaction_id": transaction_id,
        "status": payment["status"]
    }), 200

# Protected route to check payment status
@app.route('/payment-status/<transaction_id>', methods=['GET'])
@token_required
def payment_status(transaction_id):
    payment = payments.get(transaction_id)
    if not payment:
        return jsonify({"error": "Payment not found"}), 404

    return jsonify({
        "transaction_id": transaction_id,
        "status": payment["status"],
        "timestamp": payment["timestamp"]
    }), 200

# Protected route to check order status
@app.route('/order-status/<order_id>', methods=['GET'])
@token_required
def order_status(order_id):
    order = orders.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    return jsonify({
        "order_id": order_id,
        "status": order["status"],
        "items": order["items"],
        "total_amount": order["total_amount"]
    }), 200

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
