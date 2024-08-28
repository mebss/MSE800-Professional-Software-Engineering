from models.car import Car
from database import DatabaseConnection

class CarController:
    def __init__(self):
        self.db = DatabaseConnection.get_instance().connection

    def add_car(self, make, model, year, mileage, rental_rate):
        cursor = self.db.cursor()
        query = "INSERT INTO cars (make, model, year, mileage, rental_rate) VALUES (%s, %s, %s, %s, %s)"
        values = (make, model, year, mileage, rental_rate)
        cursor.execute(query, values)
        self.db.commit()
        print(f"Car '{make} {model} ({year})' added successfully.")

    def get_all_cars(self):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cars")
        cars = cursor.fetchall()
        return [Car(**car) for car in cars]

    def get_car_by_id(self, car_id):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cars WHERE car_id = %s", (car_id,))
        car = cursor.fetchone()
        if car:
            return Car(**car)
        else:
            print(f"No car found with ID {car_id}")
            return None

    def update_car(self, car_id, **kwargs):
        cursor = self.db.cursor()
        query = "UPDATE cars SET "
        query += ", ".join([f"{key} = %s" for key in kwargs.keys()])
        query += " WHERE car_id = %s"
        values = list(kwargs.values()) + [car_id]
        cursor.execute(query, tuple(values))
        self.db.commit()
        print(f"Car with ID {car_id} updated successfully.")

    def delete_car(self, car_id):
        cursor = self.db.cursor()
        
        cursor.execute("SELECT * FROM cars WHERE car_id = %s", (car_id,))
        car = cursor.fetchone()
        if car:
            print(f"Deleting car: {car}")
        else:
            print(f"No car found with ID {car_id} before deletion attempt.")
        
        cursor.execute("DELETE FROM cars WHERE car_id = %s", (car_id,))
        self.db.commit()

        cursor.execute("SELECT * FROM cars WHERE car_id = %s", (car_id,))
        car = cursor.fetchone()
        if car:
            print(f"Car with ID {car_id} was not deleted properly.")
        else:
            print(f"Car with ID {car_id} deleted successfully.")
