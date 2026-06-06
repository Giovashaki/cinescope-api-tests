import random
import string
from faker import Faker

fake = Faker()


class DataGenerator:

    @staticmethod
    def generate_movie_data():
        return {
            "name": f"Test Movie {''.join(random.choices(string.ascii_lowercase, k=8))}",
            "price": round(random.uniform(50, 1000), 2),
            "description": fake.sentence(),
            "location": random.choice(["MSK", "SPB"]),
            "published": True,
            "genreId": 1,
        }

    @staticmethod
    def generate_movie_update_data():
        return {
            "name": f"Updated {''.join(random.choices(string.ascii_lowercase, k=6))}",
            "price": round(random.uniform(50, 1000), 2),
            "description": fake.sentence(),
        }