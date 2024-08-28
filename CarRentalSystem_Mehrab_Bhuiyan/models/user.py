class User:
    def __init__(self, user_id, first_name, last_name, email, phone, role, password_hash):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.role = role  # 'admin' or 'customer'
        self.password_hash = password_hash

    def __str__(self):
        return f"User: {self.first_name} {self.last_name}, Role: {self.role}, Email: {self.email}"
