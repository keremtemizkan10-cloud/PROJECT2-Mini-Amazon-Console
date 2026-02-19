from storage import load_json, save_json, CARTS_FILE
from products import ProductManager

class CartManager:
    def __init__(self):
        self.product_manager = ProductManager()
        self.reload()

    #helper
    def _norm_pid(self, pid: str) -> str:
        return pid.strip().upper()

    def _norm_user(self, username: str) -> str:
        return username.strip()

    def _save(self):
        save_json(CARTS_FILE, self.carts)

    def reload(self):
        self.carts = load_json(CARTS_FILE, {})

    #cart operations
    def clear_cart(self, username: str):
        self.reload()
        username = self._norm_user(username)
        self.carts[username] = []
        self._save()

    def add_to_cart(self, username: str, product_id: str, quantity: int):
        self.reload()
        username = self._norm_user(username)
        product_id = self._norm_pid(product_id)

        if quantity <= 0:
            print("Quantity must be greater than 0.")
            return False

        product = self.product_manager.get_product_by_id(product_id)
        if not product:
            print("Product not found.")
            return False

        if product["stock"] < quantity:
            print("Out of stock.")
            return False

        user_cart = self.carts.get(username, [])

        for item in user_cart:
            if self._norm_pid(item["product_id"]) == product_id:
                item["qty"] += quantity
                self.carts[username] = user_cart
                self._save()
                print("Cart successfully updated.")
                return True

        user_cart.append({"product_id": product_id, "qty": quantity})
        self.carts[username] = user_cart
        self._save()
        print("Item successfully added to cart.")
        return True

    def remove_from_cart(self, username: str, product_id: str):
        self.reload()
        username = self._norm_user(username)
        product_id = self._norm_pid(product_id)

        user_cart = self.carts.get(username, [])

        updated_cart = [
            item for item in user_cart
            if self._norm_pid(item["product_id"]) != product_id
        ]

        self.carts[username] = updated_cart
        self._save()
        print("Item successfully removed from cart.")
        return True

    def remove_quantity(self, username: str, product_id: str, quantity: int):
        self.reload()
        username = self._norm_user(username)
        product_id = self._norm_pid(product_id)

        if quantity <= 0:
            print("Quantity must be greater than 0.")
            return False

        user_cart = self.carts.get(username, [])

        for item in user_cart:
            if self._norm_pid(item["product_id"]) == product_id:
                if quantity >= item["qty"]:
                    # remove fully
                    user_cart = [
                        i for i in user_cart
                        if self._norm_pid(i["product_id"]) != product_id
                    ]
                    self.carts[username] = user_cart
                    self._save()
                    print("Item successfully removed from cart.")
                    return True
                else:
                    item["qty"] -= quantity
                    self.carts[username] = user_cart
                    self._save()
                    print("Quantity reduced.")
                    return True

        print("Item not found in cart.")
        return False

    #display
    def view_cart(self, username: str):
        self.reload()
        username = self._norm_user(username)
        user_cart = self.carts.get(username, [])

        print("-- Your Cart --")

        if not user_cart:
            print("Cart is empty.\n")
            return

        #headers
        print(f"{'ID':<6} | {'Product Name':<22} | {'Qty':<4} | {'Unit €':<8} | {'Subtotal €':<10}")

        total = 0.0

        for item in user_cart:
            product = self.product_manager.get_product_by_id(item["product_id"])
            if not product:
                continue

            qty = item["qty"]
            unit = float(product["price"])
            subtotal = unit * qty
            total += subtotal

            print(
                f"{self._norm_pid(item['product_id']):<6} | "
                f"{product['name']:<22} | "
                f"{qty:<4} | "
                f"{unit:<8.2f} | "
                f"{subtotal:<10.2f}"
            )

        print()
        print(f"{'Total:':<50} €{total:.2f}")
