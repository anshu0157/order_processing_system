# Order Processing System (Backend)

## Overview
This project implements a backend system for managing and processing orders in an e-commerce platform. It provides RESTful APIs for order creation, tracking order status, and fetching key system metrics.

## Features
- **Order Management**: Create and track orders.
- **Asynchronous Processing**: Uses an in-memory queue to simulate background order processing.
- **Order Status API**: Check order statuses (Pending, Processing, Completed).
- **Metrics API**: Retrieve key system metrics like total orders processed and average processing time.

## Tech Stack
- **Backend**: Django REST Framework (DRF)
- **Database**: SQLite (default in DRF)
- **Queue**: Python `queue.Queue` (in-memory)
- **Deployment**: AWS Ec2 (optional)

---

## Installation & Setup
### 1. Clone the Repository
```sh
$ git clone https://github.com/anshu0157/order_processing_system.git
$ cd order_system
```

### 2. Create a Virtual Environment
```sh
$ python3 -m venv venv
$ source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```sh
$ pip install -r requirements.txt
```

### 4. Configure Database (SQLite by Default)
SQLite is used as the default database in DRF.
Run migrations:
```sh
$ python manage.py makemigrations
$ python manage.py migrate
```

### 5. Start the Server
```sh
$ python manage.py runserver
```

---

## API Endpoints

### 1. **Create an Order**
```http
POST /api/orders/
```
#### Request Body (JSON)
```json
{
  "user_id": 1,
  "item_ids": [101, 102],
  "total_amount": 250.75
}
```
#### Response (201 Created)
```json
{
  "message": "Order received.",
  "order_id": "ORD123"
}
```

### 2. **Check Order Status**
```http
GET /api/orders/{order_id}/status/
```
#### Response (200 OK)
```json
{
  "order_id": "ORD123",
  "status": "Processing"
}
```

### 3. **Fetch Metrics**
```http
GET /api/orders/metrics/
```
#### Response (200 OK)
```json
{
  "total_orders_processed": 150,
  "average_processing_time": "3.5s",
  "order_status_count": {
    "Pending": 10,
    "Processing": 5,
    "Completed": 135
  }
}
```

---

## Example API Requests (cURL & Postman)
### Create Order (cURL)
```sh
curl -X POST http://127.0.0.1:8000/orders/ \
     -H "Content-Type: application/json" \
     -d '{"user_id": 99, "item_ids": [101, 102], "total_amount": 250.75}'
```

### Check Order Status (Postman)
1. Open Postman
2. Make a **GET** request to `http://127.0.0.1:8000/orders/123/status/`

### Check Order metrics (Postman)
1. Open Postman
2. Make a **GET** request to `http://127.0.0.1:8000/orders/metrics/`

---

## Queue Processing
Orders are processed asynchronously using an **in-memory queue**. The worker pulls orders from the queue and updates their status.


---

## Design Decisions & Trade-offs
- **DRF for API**: Provides modular and scalable API design.
- **SQLite Database**: Chosen for simplicity; can be replaced with MySQL/PostgreSQL in production.
- **In-memory Queue**: Simulates real-world async processing.
- **Background Processing**: Can be replaced with Celery for production use.

## Assumptions
- Order processing is simulated and not instant.
- OrderId is kept as autoField as it should be unique
- In-memory queue does not persist after a server restart.
- No authentication is required for API access (can be added).

---

## Deployment (Optional)
### Deploy on AWS EC2
1. Push code to GitHub.

---

## GitHub Repository
🔗 **Repository Link:** [GitHub - Order Processing System](https://github.com/anshu0157/order_processing_system)

---

## Future Improvements
- Use **Celery + Redis** for robust async processing.
- Improve error handling and logging.
- Add **unit tests** and API documentation.

---

## Author
👨‍💻 **Anshu Kumar Singh**  
📧 anshu0157@gmail.com  
🔗 [GitHub](https://github.com/anshu0157)

