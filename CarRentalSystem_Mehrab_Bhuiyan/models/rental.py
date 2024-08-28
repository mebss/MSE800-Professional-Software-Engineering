from models.user import User
from models.car import Car
from datetime import date

class Rental:
    def __init__(self, rental_id, user: User, car: Car, rental_start_date: date, rental_end_date: date, total_cost: float):
        self.rental_id = rental_id
        self.user = user
        self.car = car
        self.rental_start_date = rental_start_date
        self.rental_end_date = rental_end_date
        self.total_cost = total_cost

    def __str__(self):
        return f"Rental ID: {self.rental_id}, User: {self.user.first_name} {self.user.last_name}, Car: {self.car.make} {self.car.model}, Start: {self.rental_start_date}, End: {self.rental_end_date}, Total: ${self.total_cost}"
