from controllers.user_controller import UserController
from controllers.car_controller import CarController
from controllers.rental_controller import RentalController
from controllers.ai_recommendation import AIRecommendation
from utils.io_utils import get_input, display_message, get_password, confirm_action

class Views:
    def __init__(self):
        self.user_controller = UserController()
        self.car_controller = CarController()
        self.rental_controller = RentalController()
        self.ai_recommendation = AIRecommendation()
        self.current_user = None

    def main_menu(self):
        while True:
            display_message("Welcome to the Car Rental System")
            choice = get_input("1. Login\n2. Register\n3. Exit\nSelect an option: ")
            if choice == '1':
                self.login()
            elif choice == '2':
                self.register()
            elif choice == '3':
                display_message("Goodbye!")
                break
            else:
                display_message("Invalid option. Please try again.")

    def login(self):
        email = get_input("Enter email: ")
        password = get_password("Enter password: ")
        user = self.user_controller.login_user(email, password)
        if user:
            self.current_user = user
            if user.role == 'admin':
                self.admin_dashboard()
            else:
                self.customer_dashboard()
        else:
            display_message("Login failed. Please check your credentials.")

    def register(self):
        first_name = get_input("Enter first name: ")
        last_name = get_input("Enter last name: ")
        email = get_input("Enter email: ")
        phone = get_input("Enter phone: ")
        password = get_password("Enter password: ")
        self.user_controller.register_user(first_name, last_name, email, phone, password)
        display_message("Registration successful. You can now log in.")

    def admin_dashboard(self):
        while True:
            display_message(f"Welcome, Admin {self.current_user.first_name}")
            choice = get_input("1. Manage Cars\n2. Manage Rentals\n3. Logout\nSelect an option: ")
            if choice == '1':
                self.manage_cars()
            elif choice == '2':
                self.manage_rentals()
            elif choice == '3':
                self.current_user = None
                break
            else:
                display_message("Invalid option. Please try again.")

    def manage_cars(self):
        while True:
            choice = get_input("1. Add Car\n2. Update Car\n3. Delete Car\n4. View All Cars\n5. Back\nSelect an option: ")
            if choice == '1':
                self.add_car()
            elif choice == '2':
                self.update_car()
            elif choice == '3':
                self.delete_car()
            elif choice == '4':
                self.view_all_cars()
            elif choice == '5':
                break
            else:
                display_message("Invalid option. Please try again.")

    def add_car(self):
        make = get_input("Enter car make: ")
        model = get_input("Enter car model: ")
        year = int(get_input("Enter car year: "))
        mileage = int(get_input("Enter car mileage: "))
        rental_rate = float(get_input("Enter rental rate per day: "))
        self.car_controller.add_car(make, model, year, mileage, rental_rate)
        display_message("Car added successfully.")

    def update_car(self):
        car_id = int(get_input("Enter car ID to update: "))
        mileage = int(get_input("Enter new mileage: "))
        rental_rate = float(get_input("Enter new rental rate: "))
        self.car_controller.update_car(car_id, mileage=mileage, rental_rate=rental_rate)
        display_message("Car updated successfully.")

    def delete_car(self):
        car_id = int(get_input("Enter car ID to delete: "))
        self.car_controller.delete_car(car_id)
        display_message("Car deleted successfully.")

    def view_all_cars(self):
        cars = self.car_controller.get_all_cars()
        for car in cars:
            print(car)

    def manage_rentals(self):
        rentals = self.rental_controller.get_all_rentals()
        if not rentals:
            display_message("No rentals to manage.")
            return
        for rental in rentals:
            print(rental)
        rental_id = int(get_input("Enter rental ID to approve/reject: "))
        choice = get_input("1. Approve\n2. Reject\nSelect an option: ")
        if choice == '1':
            self.rental_controller.approve_rental(rental_id)
            display_message("Rental approved.")
        elif choice == '2':
            self.rental_controller.reject_rental(rental_id)
            display_message("Rental rejected.")
        else:
            display_message("Invalid option. Returning to menu.")

    def customer_dashboard(self):
        while True:
            display_message(f"Welcome, {self.current_user.first_name}")
            choice = get_input("1. Browse Cars\n2. View My Bookings\n3. Get Car Recommendations\n4. Logout\nSelect an option: ")
            if choice == '1':
                self.browse_cars()
            elif choice == '2':
                self.view_bookings()
            elif choice == '3':
                self.get_recommendations()
            elif choice == '4':
                self.current_user = None
                break
            else:
                display_message("Invalid option. Please try again.")

    def browse_cars(self):
        cars = self.car_controller.get_all_cars()
        if not cars:
            display_message("No cars available.")
            return
        for car in cars:
            if car.available:
                print(car)
        car_id = int(get_input("Enter car ID to book: "))
        rental_start_date = get_input("Enter rental start date (YYYY-MM-DD): ")
        rental_end_date = get_input("Enter rental end date (YYYY-MM-DD): ")
        self.rental_controller.create_rental(self.current_user.user_id, car_id, rental_start_date, rental_end_date)
        display_message("Car booked successfully.")

    def view_bookings(self):
        rentals = self.rental_controller.get_rentals_by_user(self.current_user.user_id)
        if not rentals:
            display_message("No bookings found.")
            return
        for rental in rentals:
            print(rental)

    def get_recommendations(self):
        make = get_input("Enter preferred car make (or leave blank): ").strip()
        model = get_input("Enter preferred car model (or leave blank): ").strip()
        year_input = get_input("Enter preferred car year (or leave blank): ").strip()
        rental_rate_input = get_input("Enter maximum rental rate (or leave blank): ").strip()

        # Convert inputs to their appropriate types, or set them to None if invalid
        year = int(year_input) if year_input.isdigit() else None
        rental_rate = float(rental_rate_input) if rental_rate_input.replace('.', '', 1).isdigit() else None

        user_preferences = {
            'make': make if make and make.lower() != 'none' else None,
            'model': model if model and model.lower() != 'none' else None,
            'year': year,
            'rental_rate': rental_rate
        }

        recommendations = self.ai_recommendation.recommend_cars(user_preferences)
        if not recommendations:
            display_message("No recommendations found based on your preferences.")
        else:
            display_message("Recommended Cars:")
            for car in recommendations:
                print(car)


if __name__ == "__main__":
    views = Views()
    views.main_menu()
