from controllers.user_controller import UserController
from controllers.car_controller import CarController
from controllers.rental_controller import RentalController
from datetime import date
import mysql.connector

def reset_auto_increment():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='mehrab',
        database='car_rental_auckland'
    )
    cursor = connection.cursor()
    cursor.execute("ALTER TABLE users AUTO_INCREMENT = 1")
    cursor.execute("ALTER TABLE cars AUTO_INCREMENT = 1")
    cursor.execute("ALTER TABLE rentals AUTO_INCREMENT = 1")
    connection.commit()
    connection.close()
    print("Auto-increment values reset.")

def add_dummy_data():
    user_controller = UserController()
    car_controller = CarController()

    # Register a dummy customer
    user_controller.register_user("John", "Doe", "john.doe@example.com", "123-456-7890", "password", "customer")

    # Add a dummy car
    car_controller.add_car("Toyota", "Corolla", 2021, 10000, 45.00)

def remove_dummy_data():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='mehrab',
        database='car_rental_auckland'
    )
    cursor = connection.cursor()

    try:
        # Start by deleting all rentals that reference the dummy car and customer
        cursor.execute("DELETE FROM rentals WHERE user_id = 2 AND car_id = 1")
        connection.commit()
        print("Dummy rentals removed.")

        # Delete the dummy car
        cursor.execute("DELETE FROM cars WHERE car_id = 1")
        connection.commit()
        print("Dummy car removed.")

        # Delete the dummy user, but retain the admin
        cursor.execute("DELETE FROM users WHERE user_id = 2")
        connection.commit()
        print("Dummy user removed.")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()
    finally:
        connection.close()

def test_rental_controller():
    reset_auto_increment()

    add_dummy_data()

    rental_controller = RentalController()

    # Create a new rental
    rental_controller.create_rental(user_id=2, car_id=1, rental_start_date=date(2023, 1, 1), rental_end_date=date(2023, 1, 10))

    # Get rental by ID
    rental = rental_controller.get_rental_by_id(1)
    if rental:
        print(rental)

    # Get rentals by customer ID
    rentals = rental_controller.get_rentals_by_user(2)
    for r in rentals:
        print(r)

    # Complete a rental
    rental_controller.complete_rental(1)

    # Clean up the dummy data
    remove_dummy_data()

if __name__ == "__main__":
    test_rental_controller()
