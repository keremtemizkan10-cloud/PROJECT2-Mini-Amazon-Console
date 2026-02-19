import hashlib
from storage import load_json, save_json, USERS_FILE


class UserManager:

    def __init__(self):
        self.users = load_json(USERS_FILE, [])

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def _save(self):
        save_json(USERS_FILE, self.users)

    #new user
    def register(self, username: str, password: str) -> bool:
        if len(password) < 6:
            print("Password must be at least 6 characters.")
            return False

        if any(user["username"] == username for user in self.users):
            print("Username already exists.")
            return False

        hashed_password = self._hash_password(password)

        self.users.append({
            "username": username,
            "password": hashed_password
        })

        self._save()
        print("Registration successful.")
        return True

    #login
    def login(self, username: str, password: str) -> bool:
        hashed_password = self._hash_password(password)

        for user in self.users:
            if user["username"] == username and user["password"] == hashed_password:
                print("Login successful.")
                return True

        print("Invalid username or password.")
        return False
