import random
from faker import Faker

faker = Faker()


class DataGenerator:

    @staticmethod
    def generate_movie_data(genre_id=1):
        return {
            "name": (
                f"Test Movie {faker.unique.word()} {random.randint(1, 99999)}"
            ),
            "imageUrl": (
                f"https://picsum.photos/seed"
                f"/{random.randint(1, 10000)}/400/600"
            ),
            "price": random.randint(100, 1000),
            "description": faker.text(max_nb_chars=200),
            "location": random.choice(["MSK", "SPB"]),
            "published": True,
            "genreId": genre_id
        }
