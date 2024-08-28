import bcrypt
import sys
import os

# Add the parent directory to the sys.path to resolve the models import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user import User
from database import DatabaseConnection

class UserController:
    def __init__(self):
        self.db = DatabaseConnection.get_instance().connection
        self.ensure_default_admin()

    def ensure_default_admin(self):
        print("Checking if the default admin user exists...")
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE role = 'admin'")
        if cursor.fetchone() is None:
            print("No admin user found. Creating default admin user.")
            self.register_user(
                first_name='Admin',
                last_name='User',
                email='admin@example.com',
                phone='000-000-0000',
                password='password',  
                role='admin'
            )
            print("Default admin account created.")
        else:
            print("Admin user already exists.")

    def register_user(self, first_name, last_name, email, phone, password, role='customer'):
        print(f"Registering user: {first_name} {last_name} as {role}")
        cursor = self.db.cursor()

        # Ensure the role is either 'admin' or 'customer'
        if role not in ('admin', 'customer'):
            raise ValueError("Role must be either 'admin' or 'customer'.")

        # Hash the password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        query = """
        INSERT INTO users (first_name, last_name, email, phone, role, password_hash)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (first_name, last_name, email, phone, role, password_hash.decode('utf-8'))
        cursor.execute(query, values)
        self.db.commit()
        print(f"User '{first_name} {last_name}' registered successfully as {role}.")

    def login_user(self, email, password):
        cursor = self.db.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if user:
            stored_hash = user['password_hash'].encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                return User(**user)
            else:
                print("Login failed: Incorrect password.")
        else:
            print("Login failed: No user found with that email.")
            
        return None

    def get_user_by_id(self, user_id):
        cursor = self.db.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        if user:
            return User(**user)
        else:
            print(f"No user found with ID {user_id}")
            return None

    def get_all_users(self):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return [User(**user) for user in users]

    def update_user(self, user_id, **kwargs):
        cursor = self.db.cursor()

        if 'role' in kwargs and kwargs['role'] not in ('admin', 'customer'):
            raise ValueError("Role must be either 'admin' or 'customer'.")

        query = "UPDATE users SET "
        query += ", ".join([f"{key} = %s" for key in kwargs.keys()])
        query += " WHERE user_id = %s"
        values = list(kwargs.values()) + [user_id]
        cursor.execute(query, tuple(values))
        self.db.commit()
        print(f"User with ID {user_id} updated successfully.")

    def delete_user(self, user_id):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        self.db.commit()
        print(f"User with ID {user_id} deleted successfully.")

# Testing the UserController to check if the admin is created
if __name__ == "__main__":
    user_controller = UserController()
