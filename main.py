from storage import init_files
from users import UserManager
from products import ProductManager
from cart import CartManager
from orders import OrderManager
from ui import clear, banner, pause, read_int, read_str

def normalize_pid(pid: str) -> str:
    return pid.strip().upper()

#search flow
def search_products_flow(product_manager, cart_manager, current_user):
    while True:
        clear()
        banner()
        print("SEARCH PRODUCTS\n")

        keyword = read_str("Enter search keyword (or type 'back'): ")
        if keyword.lower() == "back":
            return

        results = product_manager.search_products_text(keyword)
        print("\n" + results)

        print("\n1) Add product to cart")
        print("2) New search")
        print("3) Return to store menu")

        choice = read_int("Choose: ", 1, 3)

        if choice == 1:
            product_id = read_str("Product ID: ")
            qty = read_int("Quantity: ", 1)
            cart_manager.add_to_cart(current_user, product_id, qty)
            pause()

        elif choice == 2:
            continue

        elif choice == 3:
            return

#browse flow
def browse_products_flow(product_manager, cart_manager, current_user):
    while True:
        clear()
        banner()
        print("BROWSE PRODUCTS\n")

        product_manager.list_products()
        print("\n1) Add product to cart")
        print("2) Return to store menu")

        choice = read_int("Choose: ", 1, 2)

        if choice == 1:
            product_id = read_str("Product ID: ").strip().upper()
            qty = read_int("Quantity: ", 1)
            cart_manager.add_to_cart(current_user, product_id, qty)

            # Optional: show quick confirmation, but NO pause screen
            input("\nAdded (or failed). Press Enter to continue...")
        
        else:
            return

#view cart flow
def view_cart_flow(product_manager, cart_manager, current_user):
    while True:
        clear()
        banner()
        print("CART\n")

        cart_manager.view_cart(current_user)

        print("\n1) Reduce quantity")
        print("2) Remove item completely")
        print("3) Return to store menu")

        choice = read_int("Choose: ", 1, 3)

        if choice == 1:
            product_id = read_str("Product ID: ").strip().upper()
            qty = read_int("Remove how many?: ", 1)
            cart_manager.remove_quantity(current_user, product_id, qty)
            input("\nPress Enter to continue...")

        elif choice == 2:
            product_id = read_str("Product ID to remove: ").strip().upper()
            cart_manager.remove_from_cart(current_user, product_id)
            input("\nPress Enter to continue...")

        else:
            return

#checkout flow
def checkout_flow(order_manager, cart_manager, current_user):
    while True:
        clear()
        banner()
        print("CHECKOUT\n")

        cart_manager.view_cart(current_user)

        print("\n1) Confirm checkout")
        print("2) Return to store menu")

        choice = read_int("Choose: ", 1, 2)

        if choice == 1:
            order_manager.checkout(current_user)
            input("\nPress Enter to return to store...")
            return

        else:
            return

#order history flow
def view_order_history_flow(order_manager, cart_manager, current_user):
    while True:
        clear()
        banner()
        print("ORDER HISTORY\n")

        order_manager.view_order_history(current_user)

        print("\n1) Return to store menu")
        choice = read_int("Choose: ", 1, 1)

        if choice == 1:
            return 

#store menu
def welcome_menu():
    clear()
    banner()
    print("1) Register")
    print("2) Login")
    print("3) Exit")
    return read_int("\nChoose: ", 1, 3)

def store_menu(username: str):
    clear()
    banner()
    print(f"Logged in as: {username}")
    print("\n1) Browse products")
    print("2) Search products")
    print("3) View cart")
    print("4) Checkout")
    print("5) View order history")
    print("6) Logout")
    return read_int("\nChoose: ", 1, 6)

def main():
    init_files()

    user_manager = UserManager()
    product_manager = ProductManager()
    cart_manager = CartManager()
    order_manager = OrderManager(product_manager, cart_manager)

    while True:
        choice = welcome_menu()

        if choice == 1:
            username = read_str("Username: ")
            password = read_str("Password: ")
            user_manager.register(username, password)
            pause()

        elif choice == 2:
            username = read_str("Username: ")
            password = read_str("Password: ")

            if not user_manager.login(username, password):
                pause()
                continue

            current_user = username

            while True:
                s_choice = store_menu(current_user)

                if s_choice == 1:
                    browse_products_flow(product_manager, cart_manager, current_user)

                elif s_choice == 2:
                    search_products_flow(product_manager, cart_manager, current_user)

                elif s_choice == 3:
                    view_cart_flow(product_manager, cart_manager, current_user)

                elif s_choice == 4:
                    checkout_flow(order_manager, cart_manager, current_user)

                elif s_choice == 5:
                    view_order_history_flow(order_manager, cart_manager, current_user)

                elif s_choice == 6:
                    break  #logout

        elif choice == 3:
            clear()
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
