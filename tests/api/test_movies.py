import allure
import pytest

from models.movies_model import MovieModel, FindAllMoviesResponse
from db.db_models import MovieDBModel
from utils.data_generator import DataGenerator


@allure.epic("Cinescope")
@allure.feature("Movies API")
@pytest.mark.api
@pytest.mark.movies
class TestMovies:

    @allure.title("GET /movies — получение списка с полной валидацией схемы")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_get_movies(self, api_manager):
        with allure.step("Отправить GET /movies"):
            response = api_manager.movies_api.get_movies()

        with allure.step("Проверить статус 200"):
            assert response.status_code == 200, \
                f"Ожидался статус 200, получен {response.status_code}"

        with allure.step("Валидировать полную схему через Pydantic"):
            movies_response = FindAllMoviesResponse(**response.json())

        with allure.step("Проверить поля пагинации"):
            assert movies_response.count >= 0
            assert movies_response.page >= 0
            assert movies_response.pageSize > 0
            assert movies_response.pageCount >= 0

    @allure.title("POST /movies — создание фильма")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_movie(self, api_manager, created_movie):
        with allure.step("Проверить что фильм создан и вернул id"):
            assert created_movie.get("id"), "ID фильма не должен быть пустым"

        with allure.step("Валидировать схему созданного фильма через Pydantic"):
            movie = MovieModel(**created_movie)
            assert movie.id
            assert movie.name

    @allure.title("GET /movies/{id} — получение фильма по id")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_get_movie_by_id(self, api_manager, created_movie):
        movie_id = created_movie["id"]

        with allure.step("Получить фильм по id"):
            response = api_manager.movies_api.get_movie_by_id(movie_id)

        with allure.step("Проверить данные фильма"):
            data = response.json()
            assert data["id"] == movie_id, \
                f"id не совпадает: ожидался {movie_id}, получен {data['id']}"
            assert data["name"] == created_movie["name"], \
                f"name не совпадает: ожидался {created_movie['name']}, получен {data['name']}"

    @allure.title("PATCH /movies/{id} — обновление фильма")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_update_movie(self, api_manager, created_movie):
        movie_id = created_movie["id"]

        with allure.step("Подготовить данные для обновления через DataGenerator"):
            update_data = DataGenerator.generate_movie_update_data()

        with allure.step("Отправить PATCH запрос"):
            response = api_manager.movies_api.update_movie(
                movie_id, update_data, expected_status=200
            )

        with allure.step("Проверить ответ"):
            data = response.json()
            assert data["id"] == movie_id, \
                f"id изменился: ожидался {movie_id}, получен {data['id']}"
            assert data["name"] == update_data["name"], \
                f"name не обновился: ожидался {update_data['name']}, получен {data['name']}"
            assert data["price"] == int(update_data["price"]), \
                f"price не обновился: ожидался {int(update_data['price'])}, получен {data['price']}"

    @allure.title("DELETE /movies/{id} — удаление фильма")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_delete_movie(self, api_manager):
        with allure.step("Создать фильм"):
            movie_data = DataGenerator.generate_movie_data()
            response = api_manager.movies_api.create_movie(movie_data)
            assert response.status_code == 201
            movie_id = response.json()["id"]

        with allure.step("Удалить фильм"):
            api_manager.movies_api.delete_movie(movie_id, expected_status=200)

        with allure.step("Проверить что фильм больше не доступен"):
            api_manager.movies_api.get_movie_by_id(movie_id, expected_status=404)

    @allure.title("GET /movies/{id} — получение несуществующего фильма")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_get_movie_by_invalid_id(self, api_manager):
        with allure.step("Запросить фильм с несуществующим id"):
            api_manager.movies_api.get_movie_by_id(999999999, expected_status=404)

    @allure.title("POST /movies — создание фильма без name")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_create_movie_without_name(self, api_manager):
        with allure.step("Подготовить данные без поля name"):
            movie_data = DataGenerator.generate_movie_data()
            del movie_data["name"]

        with allure.step("Отправить запрос и ожидать 400"):
            api_manager.movies_api.create_movie(movie_data, expected_status=400)

    @allure.title("POST /movies — создание фильма без price")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_create_movie_without_price(self, api_manager):
        with allure.step("Подготовить данные без поля price"):
            movie_data = DataGenerator.generate_movie_data()
            del movie_data["price"]

        with allure.step("Отправить запрос и ожидать 400"):
            api_manager.movies_api.create_movie(movie_data, expected_status=400)

    @allure.title("POST /movies — создание дубликата фильма")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_create_duplicate_movie(self, api_manager, created_movie):
        with allure.step("Подготовить данные с существующим именем"):
            duplicate_data = DataGenerator.generate_movie_data()
            duplicate_data["name"] = created_movie["name"]

        with allure.step("Отправить запрос и ожидать 409"):
            api_manager.movies_api.create_movie(duplicate_data, expected_status=409)

    @allure.title("GET /movies с фильтром {param_name}={param_value}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.parametrize("param_name,param_value", [
        ("page", 1),
        ("pageSize", 5),
        ("pageSize", 10),
        ("published", True),
        ("published", False),
    ], ids=[
        "page=1",
        "pageSize=5",
        "pageSize=10",
        "published=true",
        "published=false",
    ])
    def test_get_movies_with_filter(self, api_manager, param_name, param_value):
        with allure.step(f"Отправить GET /movies?{param_name}={param_value}"):
            response = api_manager.movies_api.get_movies(
                params={param_name: param_value}
            )

        with allure.step("Проверить статус 200"):
            assert response.status_code == 200, \
                f"Ожидался статус 200, получен {response.status_code}"

        with allure.step("Валидировать схему ответа через Pydantic"):
            movies_response = FindAllMoviesResponse(**response.json())

        with allure.step("Проверить что фильтр отражён в ответе"):
            if param_name == "pageSize":
                assert movies_response.pageSize == param_value
            if param_name == "page":
                assert movies_response.page == param_value

    @allure.title("POST /movies — проверка записи в БД после создания и удаления")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.db
    def test_create_movie_check_db(self, api_manager, db_session):
        movie_data = DataGenerator.generate_movie_data()

        with allure.step("Убедиться что фильма ещё нет в БД"):
            existing = db_session.query(MovieDBModel).filter(
                MovieDBModel.name == movie_data["name"]
            ).first()
            assert existing is None, \
                f"Фильм '{movie_data['name']}' уже существует в БД до создания"

        with allure.step("Создать фильм через API"):
            response = api_manager.movies_api.create_movie(movie_data)
            assert response.status_code == 201
            movie_id = response.json()["id"]

        with allure.step("Проверить что фильм появился в БД"):
            db_session.expire_all()
            db_movie = db_session.query(MovieDBModel).filter(
                MovieDBModel.id == movie_id
            ).first()
            assert db_movie is not None, \
                f"Фильм id={movie_id} не найден в БД после создания"
            assert db_movie.name == movie_data["name"]

        with allure.step("Удалить фильм через API"):
            api_manager.movies_api.delete_movie(movie_id, expected_status=200)

        with allure.step("Проверить что фильм удалён из БД"):
            db_session.expire_all()
            deleted = db_session.query(MovieDBModel).filter(
                MovieDBModel.id == movie_id
            ).first()
            assert deleted is None, \
                f"Фильм id={movie_id} всё ещё в БД после удаления"