import os

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print("-" * 32)
    print("        Mini Amazon")
    print("-" * 32)

def pause():
    input("\nPress Enter to continue...")

def read_int(prompt: str, min_val=None, max_val=None):
    while True:
        value = input(prompt).strip()
        try:
            n = int(value)
            if min_val is not None and n < min_val:
                print(f"Must be >= {min_val}")
                continue
            if max_val is not None and n > max_val:
                print(f"Must be <= {max_val}")
                continue
            return n
        except ValueError:
            print("Please enter a valid integer.")

def read_str(prompt: str, allow_empty=False):
    while True:
        s = input(prompt).strip()
        if not s and not allow_empty:
            print("Input cannot be empty.")
            continue
        return s
