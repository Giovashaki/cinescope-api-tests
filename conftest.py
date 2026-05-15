import pytest
import requests
from clients.api_manager import ApiManager
from constants import ADMIN_EMAIL, ADMIN_PASSWORD
from utils.data_generator import DataGenerator


@pytest.fixture(scope="session")
def session():
    """Создаём одну HTTP сессию для всех тестов"""
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session):
    manager = ApiManager(session)
    manager.auth_api.authenticate(ADMIN_EMAIL, ADMIN_PASSWORD)
    return manager


@pytest.fixture
def created_movie(api_manager):
    movie_data = DataGenerator.generate_movie_data()
    response = api_manager.movies_api.create_movie(movie_data)
    movie = response.json()
    movie_id = movie["id"]
    yield movie
    api_manager.movies_api.delete_movie(movie_id, expected_status=200)
