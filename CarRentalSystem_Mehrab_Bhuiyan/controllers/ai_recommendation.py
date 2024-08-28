from models.car import Car
from database import DatabaseConnection

class AIRecommendation:
    def __init__(self):
        self.db = DatabaseConnection.get_instance().connection

    def recommend_cars(self, user_preferences, top_n=5):
        """
        Recommends cars based on user preferences.

        :param user_preferences: A dictionary containing user preferences (e.g., make, model, year).
        :param top_n: Number of top recommendations to return.
        :return: A list of recommended Car objects.
        """
        cursor = self.db.cursor(dictionary=True)
        query = "SELECT * FROM cars WHERE available = 1"
        cursor.execute(query)
        available_cars = cursor.fetchall()

        # Filter cars based on user preferences
        filtered_cars = self._filter_cars_by_preferences(available_cars, user_preferences)

        # Rank cars based on some criteria (e.g., year, rental rate)
        ranked_cars = self._rank_cars(filtered_cars)

        # Return the top N recommendations
        return ranked_cars[:top_n]

    def _filter_cars_by_preferences(self, cars, user_preferences):
        """
        Filters the list of cars based on user preferences.

        :param cars: List of car dictionaries fetched from the database.
        :param user_preferences: Dictionary containing user preferences.
        :return: List of filtered car dictionaries.
        """
        filtered_cars = []
        for car in cars:
            if user_preferences.get('make') and user_preferences['make'].strip().lower() != '' and user_preferences['make'].lower() != 'none':
                if car['make'].lower() != user_preferences['make'].lower():
                    continue
            if user_preferences.get('model') and user_preferences['model'].strip().lower() != '' and user_preferences['model'].lower() != 'none':
                if car['model'].lower() != user_preferences['model'].lower():
                    continue
            if user_preferences.get('year') and user_preferences['year'] != 0:
                if car['year'] != user_preferences['year']:
                    continue
            if user_preferences.get('rental_rate') and user_preferences['rental_rate'] != 0.0:
                if car['rental_rate'] > user_preferences['rental_rate']:
                    continue
            filtered_cars.append(Car(**car))
        return filtered_cars

    def _rank_cars(self, cars):
        """
        Ranks the cars based on year and rental rate.

        :param cars: List of Car objects.
        :return: List of ranked Car objects.
        """
        # Simple ranking: Newer cars first, then by rental rate (lower is better)
        return sorted(cars, key=lambda car: (car.year, car.rental_rate), reverse=True)

    def recommend_based_on_rental_history(self, user_id, top_n=5):
        """
        Recommends cars based on the user's rental history.

        :param user_id: The ID of the user.
        :param top_n: Number of top recommendations to return.
        :return: A list of recommended Car objects.
        """
        cursor = self.db.cursor(dictionary=True)

        # Fetch the user's rental history
        query = """
        SELECT cars.*
        FROM rentals
        JOIN cars ON rentals.car_id = cars.car_id
        WHERE rentals.user_id = %s
        """
        cursor.execute(query, (user_id,))
        rented_cars = cursor.fetchall()

        # If the user has no rental history, recommend the most popular cars
        if not rented_cars:
            return self.recommend_cars({}, top_n)

        # Find the most common make and model in the user's rental history
        favorite_make = self._most_common([car['make'] for car in rented_cars])
        favorite_model = self._most_common([car['model'] for car in rented_cars])

        # Use these preferences to recommend similar cars
        user_preferences = {
            'make': favorite_make,
            'model': favorite_model
        }
        return self.recommend_cars(user_preferences, top_n)

    def _most_common(self, lst):
        """
        Helper function to find the most common element in a list.

        :param lst: List of elements.
        :return: The most common element.
        """
        return max(set(lst), key=lst.count)
