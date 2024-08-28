from models.rental import Rental
from models.user import User
from models.car import Car
from database import DatabaseConnection
from datetime import datetime


class RentalController:
    def __init__(self):
        self.db = DatabaseConnection.get_instance().connection

    def create_rental(self, user_id, car_id, rental_start_date, rental_end_date):
        # Convert the string dates into date objects
        rental_start_date = datetime.strptime(rental_start_date, "%Y-%m-%d").date()
        rental_end_date = datetime.strptime(rental_end_date, "%Y-%m-%d").date()

        cursor = self.db.cursor()
        cursor.execute("SELECT rental_rate FROM cars WHERE car_id = %s", (car_id,))
        rental_rate = cursor.fetchone()[0]
        rental_days = (rental_end_date - rental_start_date).days
        total_cost = rental_rate * rental_days

        query = """
        INSERT INTO rentals (user_id, car_id, rental_start_date, rental_end_date, total_cost)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (user_id, car_id, rental_start_date, rental_end_date, total_cost)
        cursor.execute(query, values)
        self.db.commit()

        cursor.execute("UPDATE cars SET available = FALSE WHERE car_id = %s", (car_id,))
        self.db.commit()

        print(f"Rental created successfully for car ID {car_id} and user ID {user_id}.")

    def get_rental_by_id(self, rental_id):
        cursor = self.db.cursor(dictionary=True)
        query = """
        SELECT rentals.*, users.*, cars.*
        FROM rentals
        JOIN users ON rentals.user_id = users.user_id
        JOIN cars ON rentals.car_id = cars.car_id
        WHERE rental_id = %s
        """
        cursor.execute(query, (rental_id,))
        rental = cursor.fetchone()

        if rental:
            user = User(
                user_id=rental['user_id'],
                first_name=rental['first_name'],
                last_name=rental['last_name'],
                email=rental['email'],
                phone=rental['phone'],
                role=None,
                password_hash=None
            )

            car = Car(
                car_id=rental['car_id'],
                make=rental['make'],
                model=rental['model'],
                year=rental['year'],
                mileage=rental['mileage'],
                rental_rate=rental['rental_rate'],
                available=rental['available']
            )

            return Rental(
                rental_id=rental['rental_id'],
                user=user,
                car=car,
                rental_start_date=rental['rental_start_date'],
                rental_end_date=rental['rental_end_date'],
                total_cost=rental['total_cost']
            )
        else:
            print(f"No rental found with ID {rental_id}")
            return None

    def get_all_rentals(self):
        cursor = self.db.cursor(dictionary=True)
        query = """
        SELECT rentals.*, users.*, cars.*
        FROM rentals
        JOIN users ON rentals.user_id = users.user_id
        JOIN cars ON rentals.car_id = cars.car_id
        """
        cursor.execute(query)
        rentals = cursor.fetchall()

        rental_list = []
        for rental in rentals:
            user = User(
                user_id=rental['user_id'],
                first_name=rental['first_name'],
                last_name=rental['last_name'],
                email=rental['email'],
                phone=rental['phone'],
                role=None,
                password_hash=None
            )

            car = Car(
                car_id=rental['car_id'],
                make=rental['make'],
                model=rental['model'],
                year=rental['year'],
                mileage=rental['mileage'],
                rental_rate=rental['rental_rate'],
                available=rental['available']
            )

            rental_list.append(Rental(
                rental_id=rental['rental_id'],
                user=user,
                car=car,
                rental_start_date=rental['rental_start_date'],
                rental_end_date=rental['rental_end_date'],
                total_cost=rental['total_cost']
            ))

        return rental_list

    def get_rentals_by_user(self, user_id):
        cursor = self.db.cursor(dictionary=True)
        query = """
        SELECT rentals.*, users.*, cars.*
        FROM rentals
        JOIN users ON rentals.user_id = users.user_id
        JOIN cars ON rentals.car_id = cars.car_id
        WHERE rentals.user_id = %s
        """
        cursor.execute(query, (user_id,))
        rentals = cursor.fetchall()

        rental_list = []
        for rental in rentals:
            user = User(
                user_id=rental['user_id'],
                first_name=rental['first_name'],
                last_name=rental['last_name'],
                email=rental['email'],
                phone=rental['phone'],
                role=None,
                password_hash=None
            )

            car = Car(
                car_id=rental['car_id'],
                make=rental['make'],
                model=rental['model'],
                year=rental['year'],
                mileage=rental['mileage'],
                rental_rate=rental['rental_rate'],
                available=rental['available']
            )

            rental_list.append(Rental(
                rental_id=rental['rental_id'],
                user=user,
                car=car,
                rental_start_date=rental['rental_start_date'],
                rental_end_date=rental['rental_end_date'],
                total_cost=rental['total_cost']
            ))

        return rental_list

    def complete_rental(self, rental_id):
        cursor = self.db.cursor()
        cursor.execute("SELECT car_id FROM rentals WHERE rental_id = %s", (rental_id,))
        car_id = cursor.fetchone()[0]
        cursor.execute("UPDATE cars SET available = TRUE WHERE car_id = %s", (car_id,))
        self.db.commit()

        print(f"Rental with ID {rental_id} has been completed and car with ID {car_id} is now available.")

    def approve_rental(self, rental_id):
        cursor = self.db.cursor()
        query = "UPDATE rentals SET status = 'approved' WHERE rental_id = %s"
        cursor.execute(query, (rental_id,))
        self.db.commit()
        print(f"Rental with ID {rental_id} has been approved.")

    def reject_rental(self, rental_id):
        cursor = self.db.cursor()
        query = "UPDATE rentals SET status = 'rejected' WHERE rental_id = %s"
        cursor.execute(query, (rental_id,))
        self.db.commit()
        print(f"Rental with ID {rental_id} has been rejected.")

    def get_pending_rentals(self):
        cursor = self.db.cursor(dictionary=True)
        query = "SELECT * FROM rentals WHERE status = 'pending'"
        cursor.execute(query)
        rentals = cursor.fetchall()
        return [Rental(**rental) for rental in rentals]
