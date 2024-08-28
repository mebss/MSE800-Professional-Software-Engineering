class Car:
    def __init__(self, car_id, make, model, year, mileage, rental_rate, available=True):
        self.car_id = car_id
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage
        self.rental_rate = rental_rate
        self.available = available

    def __str__(self):
        return f"{self.make} {self.model} ({self.year}) - ${self.rental_rate}/day, Available: {self.available}"
