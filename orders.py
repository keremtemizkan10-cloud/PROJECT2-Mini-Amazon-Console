import datetime
from storage import load_json, save_json, ORDERS_FILE

class OrderManager:

    def __init__(self, product_manager, cart_manager):
        self.product_manager = product_manager
        self.cart_manager = cart_manager
        self.orders = load_json(ORDERS_FILE, [])

    def _save(self):
        save_json(ORDERS_FILE, self.orders)

    def _generate_order_id(self):
        return f"O{len(self.orders) + 1:04d}"

    def checkout(self, username: str):
        self.cart_manager.reload()
        user_cart = self.cart_manager.carts.get(username, [])

        if not user_cart:
            print("Cart is empty.")
            return False

        for item in user_cart:
            product = self.product_manager.get_product_by_id(item["product_id"])
            if not product or product["stock"] < item["qty"]:
                print("Stock issue detected.")
                return False

        total = 0
        order_items = []

        for item in user_cart:
            product = self.product_manager.get_product_by_id(item["product_id"])
            self.product_manager.reduce_stock(item["product_id"], item["qty"])

            subtotal = product["price"] * item["qty"]
            total += subtotal

            order_items.append({
                "product_id": item["product_id"],
                "name": product["name"],
                "qty": item["qty"],
                "unit_price": product["price"]
            })

        order = {
            "order_id": self._generate_order_id(),
            "username": username,
            "items": order_items,
            "total": total,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        self.orders.append(order)
        self._save()

        self.cart_manager.clear_cart(username)

        print("\nCheckout successful!")
        print(f"Order ID: {order['order_id']}\n")

        print(f"{'ID':<6} | {'Product Name':<22} | {'Qty':<4} | {'Unit €':<8} | {'Subtotal €':<10}")

        for it in order_items:
            subtotal = it["unit_price"] * it["qty"]
            print(
                f"{it['product_id']:<6} | "
                f"{it['name']:<22} | "
                f"{it['qty']:<4} | "
                f"{it['unit_price']:<8.2f} | "
                f"{subtotal:<10.2f}"
            )

        print()
        print(f"{'Total:':<50} €{total:.2f}")

        return True

    def view_order_history(self, username: str):
        user_orders = [o for o in self.orders if o["username"] == username]

        if not user_orders:
            print("No orders found.")
            return

        print("\n--- Order History ---")
        for order in user_orders:
            print(f"\nOrder ID: {order['order_id']}")
            print(f"Date: {order['timestamp']}")
            print(f"Total: €{order['total']:.2f}")
            
            print("Items:")
        for it in order["items"]:
            print(f"- {it['product_id']} | {it['name']} | Qty: {it['qty']} | €{it['unit_price']:.2f}")

