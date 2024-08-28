from models.car import Car
from models.user import User
from models.rental import Rental
from datetime import date

# Test Car Model
def test_car_model():
    car = Car(car_id=1, make="Toyota", model="Corolla", year=2020, mileage=15000, rental_rate=40.00)
    print(car)
    assert car.make == "Toyota"
    assert car.model == "Corolla"
    assert car.year == 2020
    assert car.rental_rate == 40.00
    assert car.available is True

# Test User Model
def test_user_model():
    user = User(user_id=1, first_name="John", last_name="Doe", email="johndoe@example.com", phone="123-456-7890", role="customer", password_hash="hashed_password")
    print(user)
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "johndoe@example.com"
    assert user.phone == "123-456-7890"
    assert user.role == "customer"

# Test Rental Model
def test_rental_model():
    car = Car(car_id=1, make="Toyota", model="Corolla", year=2020, mileage=15000, rental_rate=40.00)
    user = User(user_id=1, first_name="John", last_name="Doe", email="johndoe@example.com", phone="123-456-7890", role="customer", password_hash="hashed_password")
    rental = Rental(rental_id=1, user=user, car=car, rental_start_date=date(2023, 1, 1), rental_end_date=date(2023, 1, 10), total_cost=400.00)
    print(rental)
    assert rental.user == user
    assert rental.car == car
    assert rental.total_cost == 400.00

# Run the tests
if __name__ == "__main__":
    test_car_model()
    test_user_model()
    test_rental_model()

    print("All tests passed successfully!")
