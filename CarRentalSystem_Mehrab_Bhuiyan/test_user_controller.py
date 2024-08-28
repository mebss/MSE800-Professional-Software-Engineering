import unittest
from controllers.user_controller import UserController
from models.user import User

class TestUserController(unittest.TestCase):

    def setUp(self):
        # This will reset the database to a known state before each test.
        self.user_controller = UserController()
        self.user_controller.db.cursor().execute("DELETE FROM users")
        self.user_controller.db.commit()

    def tearDown(self):
        # Cleanup after each test
        self.user_controller.db.cursor().execute("DELETE FROM users")
        self.user_controller.db.commit()

    def test_register_user(self):
        self.user_controller.register_user(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="123-456-7890",
            password="password",
            role="customer"
        )

        user = self.user_controller.get_user_by_id(1)
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertEqual(user.role, "customer")

    def test_admin_creation(self):
        # Ensure default admin is created
        admin = self.user_controller.get_all_users()[0]
        self.assertEqual(admin.email, "admin@example.com")
        self.assertEqual(admin.role, "admin")

    def test_login_user(self):
        self.user_controller.register_user(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="123-456-7890",
            password="password",
            role="customer"
        )

        # Test correct login
        user = self.user_controller.login_user("john.doe@example.com", "password")
        self.assertIsNotNone(user)

        # Test incorrect login
        user = self.user_controller.login_user("john.doe@example.com", "wrongpassword")
        self.assertIsNone(user)

    def test_delete_user(self):
        self.user_controller.register_user(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="123-456-7890",
            password="password",
            role="customer"
        )

        self.user_controller.delete_user(1)
        user = self.user_controller.get_user_by_id(1)
        self.assertIsNone(user)

if __name__ == "__main__":
    unittest.main()
