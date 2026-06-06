import pytest
import requests
from sqlalchemy.orm import Session

from clients.api_manager import ApiManager
from constants import ADMIN_EMAIL, ADMIN_PASSWORD
from utils.data_generator import DataGenerator
from db.db_client import get_db_session


@pytest.fixture(scope="session")
def session():
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


@pytest.fixture(scope="module")
def db_session() -> Session:
    db = get_db_session()
    yield db
    db.close()