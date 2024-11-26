

# Bakery Payment Web Service

A Flask-based web service for managing bakery orders and payments with JWT-based authentication.

## Features
- **User Login:** Obtain a token using `/login`.
- **Create Orders:** Submit bakery orders with `/create-order` (authenticated).
- **Initiate Payments:** Start payments for orders with `/initiate-payment` (authenticated).
- **Order & Payment Status:** Check statuses via `/order-status/<order_id>` and `/payment-status/<transaction_id>` (authenticated).

## Setup
1. Install dependencies:  
   ```bash
   pip install flask pyjwt
   ```
2. Run the service:  
   ```bash
   python bakery_service.py
   ```
3. Access via `http://127.0.0.1:5000`.

## Endpoints
- `POST /login`  
  Input: `{ "username": "string", "password": "string" }`  
  Output: JWT token.
  
- `POST /create-order`  
  Input: `{ "bakery_name": "string", "items": "list", "total_amount": "number" }`  
  Output: Order ID.

- `POST /initiate-payment`  
  Input: `{ "order_id": "string" }`  
  Output: Transaction ID.

- `GET /order-status/<order_id>`  
  Output: Order details.

- `GET /payment-status/<transaction_id>`  
  Output: Payment details.

## Notes
- Update `SECRET_KEY` in the script for better security.
- Requires Python 3.7+.

