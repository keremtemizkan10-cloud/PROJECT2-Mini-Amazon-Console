# Mini-Amazon Console Application

This project is a console-based mini e-commerce system developed in Python.  
The goal was to simulate a small online store where users can register, log in, browse products, manage a cart, and place orders.

The system is modular and uses JSON files for persistent data storage.

---

## Features

### User Management
- User registration with username validation
- Password length validation (minimum 6 characters)
- Secure login system
- Password hashing using SHA-256

### Product Management
- List available products
- Search products by keyword (case-insensitive)
- View product stock levels
- Automatic stock reduction after checkout

### Cart System
- Each user has an individual cart
- Add products with quantity validation
- Reduce quantity or remove items completely
- Cart persists between sessions

### Checkout System
- Stock is re-validated before checkout
- Orders are saved with:
  - Unique order ID
  - Purchased items
  - Total price
  - Timestamp
- Cart is cleared after successful checkout

---

## Project Structure

PROJECT2
│
|- main.py
|- users.py
|- products.py
|- cart.py
|- orders.py
|- storage.py
|- ui.py
|- data
  |- users.json
  |- products.json
  |- carts.json
  |- orders.json

---

## How to Run

Make sure Python 3 is installed.

Run the following command inside the project folder:

```bash
python main.py
