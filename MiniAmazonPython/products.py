from storage import load_json, save_json, PRODUCTS_FILE

class ProductManager:
    def __init__(self):
        self.products = load_json(PRODUCTS_FILE, [])

    def _save(self):
        save_json(PRODUCTS_FILE, self.products)

    #helpers
    def _search(self, keyword: str):
        keyword = keyword.lower()
        return [p for p in self.products if keyword in p["name"].lower()]

    def _format_products_table(self, products, title: str) -> str:
        if not products:
            return "No products available." if "Available" in title else "No matching products found."

        lines = []
        lines.append(f"\n{title}\n")

        #headers
        lines.append(f"{'ID':<6} | {'Product Name':<22} | {'Price (€)':<10} | {'Stock':<5}")
        lines.append("-" * 55)

        #rows
        for p in products:
            lines.append(
                f"{p['product_id']:<6} | "
                f"{p['name']:<22} | "
                f"€{p['price']:<8.2f} | "
                f"{p['stock']:<5}"
            )

        return "\n".join(lines)

    #list
    def list_products(self):
        print(self.list_products_text())

    def list_products_text(self) -> str:
        return self._format_products_table(self.products, "--- Available Products ---")

    #search
    def search_products(self, keyword: str):
        print(self.search_products_text(keyword))

    def search_products_text(self, keyword: str) -> str:
        results = self._search(keyword)
        return self._format_products_table(results, "--- Search Results ---")

    #product id
    def get_product_by_id(self, product_id: str):
        pid = product_id.strip().upper()
        for product in self.products:
            if product["product_id"].strip().upper() == pid:
                return product
        return None

    #stock
    def reduce_stock(self, product_id: str, quantity: int):
        product = self.get_product_by_id(product_id)
        if product and product["stock"] >= quantity:
            product["stock"] -= quantity
            self._save()
            return True
        return False
