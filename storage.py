# storage.py
import json
import os
from typing import Any

# Absolute base directory (project folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

USERS_FILE = os.path.join(DATA_DIR, "users.json")
PRODUCTS_FILE = os.path.join(DATA_DIR, "products.json")
CARTS_FILE = os.path.join(DATA_DIR, "carts.json")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")


def ensure_data_dir() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)


def load_json(filepath: str, default: Any) -> Any:
    ensure_data_dir()

    if not os.path.exists(filepath):
        return default

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return default
            return json.loads(content)
    except (json.JSONDecodeError, OSError):
        return default


def save_json(filepath: str, data: Any) -> None:
    ensure_data_dir()

    tmp_path = filepath + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp_path, filepath)


def init_files() -> None:
    ensure_data_dir()

    if not os.path.exists(USERS_FILE):
        save_json(USERS_FILE, [])

    if not os.path.exists(PRODUCTS_FILE):
        sample_products = [
            {"product_id": "P1001", "name": "USB-C Cable", "price": 9.99, "stock": 30},
            {"product_id": "P1002", "name": "Wireless Mouse", "price": 19.99, "stock": 15},
            {"product_id": "P1003", "name": "Mechanical Keyboard", "price": 59.99, "stock": 8},
        ]
        save_json(PRODUCTS_FILE, sample_products)

    if not os.path.exists(CARTS_FILE):
        save_json(CARTS_FILE, {})

    if not os.path.exists(ORDERS_FILE):
        save_json(ORDERS_FILE, [])
