import math
from collections import Counter

def calculate_similarity(car1, car2):
    """
    Calculate a simple similarity score between two cars based on their attributes.
    This could be enhanced with more sophisticated techniques (e.g., cosine similarity, etc.)
    """
    score = 0
    
    if car1.make.lower() == car2.make.lower():
        score += 1
    if car1.model.lower() == car2.model.lower():
        score += 1
    if car1.year == car2.year:
        score += 1
    if car1.mileage and car2.mileage:
        mileage_diff = abs(car1.mileage - car2.mileage)
        score += max(0, 1 - (mileage_diff / max(car1.mileage, car2.mileage)))
    if car1.rental_rate and car2.rental_rate:
        rate_diff = abs(car1.rental_rate - car2.rental_rate)
        score += max(0, 1 - (rate_diff / max(car1.rental_rate, car2.rental_rate)))
    
    return score

def find_most_similar_car(cars, target_car):
    """
    Find the most similar car to the target car in the list of cars.
    """
    best_match = None
    highest_score = -math.inf

    for car in cars:
        if car.car_id != target_car.car_id:
            similarity_score = calculate_similarity(car, target_car)
            if similarity_score > highest_score:
                highest_score = similarity_score
                best_match = car

    return best_match

def aggregate_preferences(preferences_list):
    """
    Aggregate preferences from multiple users into a single preference profile.
    This could be based on simple majority voting or more sophisticated aggregation techniques.
    """
    aggregated_preferences = Counter()

    for preferences in preferences_list:
        for key, value in preferences.items():
            if value and value.lower() != 'none':
                aggregated_preferences[(key, value.lower())] += 1
    
    return dict(aggregated_preferences.most_common())

def filter_cars_by_preferences(cars, preferences):
    """
    Filter cars based on user preferences.
    """
    filtered_cars = []

    for car in cars:
        match = True
        for key, value in preferences.items():
            if value and value.lower() != 'none':
                if getattr(car, key).lower() != value.lower():
                    match = False
                    break
        if match:
            filtered_cars.append(car)

    return filtered_cars

def sort_cars_by_similarity(cars, reference_car):
    """
    Sort cars by their similarity to a reference car.
    """
    cars.sort(key=lambda car: calculate_similarity(car, reference_car), reverse=True)
    return cars

def generate_recommendations(cars, user_preferences, num_recommendations=5):
    """
    Generate a list of recommended cars based on user preferences.
    """
    filtered_cars = filter_cars_by_preferences(cars, user_preferences)
    if not filtered_cars:
        return []

    
    reference_car = Car(car_id=0, **{key: value for key, value in user_preferences.items() if value and value.lower() != 'none'})
    
    sorted_cars = sort_cars_by_similarity(filtered_cars, reference_car=reference_car)
    return sorted_cars[:num_recommendations]
