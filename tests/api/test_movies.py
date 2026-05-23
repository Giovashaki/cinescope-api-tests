from utils.data_generator import DataGenerator


class TestMoviesApi:

    def test_get_movies(self, api_manager):
        response = api_manager.movies_api.get_movies()
        data = response.json()

        assert "movies" in data
        assert "count" in data
        assert isinstance(data["movies"], list)
        for movie in data["movies"]:
            assert "id" in movie
            assert "name" in movie
            assert "price" in movie
            assert "location" in movie

    def test_get_movies_with_filter_by_location(self, api_manager):
        params = {"locations": "MSK"}
        response = api_manager.movies_api.get_movies(params=params)
        data = response.json()

        assert "movies" in data
        assert len(data["movies"]) > 0
        for movie in data["movies"]:
            assert movie["location"] == "MSK"

    def test_get_movies_with_filter_by_price(self, api_manager):
        params = {"minPrice": 100, "maxPrice": 500}
        response = api_manager.movies_api.get_movies(params=params)
        data = response.json()

        assert "movies" in data
        assert len(data["movies"]) > 0
        for movie in data["movies"]:
            assert 100 <= movie["price"] <= 500

    def test_create_movie(self, api_manager):
        movie_data = DataGenerator.generate_movie_data()
        response = api_manager.movies_api.create_movie(movie_data)
        data = response.json()

        assert "id" in data
        assert data["name"] == movie_data["name"]
        assert data["price"] == movie_data["price"]
        assert data["location"] == movie_data["location"]

        api_manager.movies_api.delete_movie(data["id"])

    def test_get_movie_by_id(self, api_manager, created_movie):
        movie_id = created_movie["id"]
        response = api_manager.movies_api.get_movie_by_id(movie_id)
        data = response.json()

        assert data["id"] == movie_id
        assert data["name"] == created_movie["name"]

    def test_update_movie(self, api_manager, created_movie):
        movie_id = created_movie["id"]
        update_data = {
            "name": f"Updated {created_movie['name']}",
            "price": 999
        }
        response = api_manager.movies_api.update_movie(movie_id, update_data)
        data = response.json()

        assert data["name"] == update_data["name"]
        assert data["price"] == update_data["price"]
        assert data["location"] == created_movie["location"]
        assert data["genreId"] == created_movie["genreId"]

    def test_delete_movie(self, api_manager):
        movie_data = DataGenerator.generate_movie_data()
        created = api_manager.movies_api.create_movie(movie_data).json()
        movie_id = created["id"]

        api_manager.movies_api.delete_movie(movie_id)
        api_manager.movies_api.get_movie_by_id(movie_id, expected_status=404)

    def test_get_movie_by_invalid_id(self, api_manager):
        api_manager.movies_api.get_movie_by_id(999999999, expected_status=404)

    def test_create_movie_without_name(self, api_manager):
        movie_data = DataGenerator.generate_movie_data()
        del movie_data["name"]

        api_manager.movies_api.create_movie(movie_data, expected_status=400)

    def test_create_movie_without_price(self, api_manager):
        movie_data = DataGenerator.generate_movie_data()
        del movie_data["price"]

        api_manager.movies_api.create_movie(movie_data, expected_status=400)

    def test_create_duplicate_movie(self, api_manager, created_movie):
        duplicate_data = DataGenerator.generate_movie_data()
        duplicate_data["name"] = created_movie["name"]

        api_manager.movies_api.create_movie(
            duplicate_data, expected_status=409
        )