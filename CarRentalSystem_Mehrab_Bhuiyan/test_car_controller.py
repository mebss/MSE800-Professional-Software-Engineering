from controllers.car_controller import CarController
from database import DatabaseConnection

def reset_auto_increment():
    connection = DatabaseConnection.get_instance().connection
    cursor = connection.cursor()
    cursor.execute("ALTER TABLE cars AUTO_INCREMENT = 1")
    connection.commit()
    print("Auto-increment reset to 1 for 'cars' table.")

def test_car_controller():
    car_controller = CarController()

    # Add a new car
    car_controller.add_car("Honda", "Civic", 2021, 5000, 50.00)

    # Get all cars
    cars = car_controller.get_all_cars()
    print("Cars after addition:")
    for car in cars:
        print(car)

    # Get a specific car by ID
    car = car_controller.get_car_by_id(1)
    if car:
        print(f"Retrieved car with ID 1: {car}")

    # Update a car's mileage
    car_controller.update_car(1, mileage=6000)
    print("Car with ID 1 after update:")
    car = car_controller.get_car_by_id(1)
    print(car)

    # Delete a car by ID
    car_controller.delete_car(1)
    print("Car with ID 1 deleted.")

    # Reset auto-increment after deletion
    reset_auto_increment()

    # Verify the car is deleted
    car = car_controller.get_car_by_id(1)
    if car is None:
        print("Car with ID 1 successfully deleted.")
    else:
        print("Car with ID 1 still exists in the database.")

    # Check all cars after deletion
    cars = car_controller.get_all_cars()
    print("Cars after deletion:")
    for car in cars:
        print(car)

if __name__ == "__main__":
    test_car_controller()
