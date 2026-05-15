from clients.auth_api import AuthAPI
from clients.movies_api import MoviesAPI


class ApiManager:

    def __init__(self, session):
        self.session = session
        self.auth_api = AuthAPI(session)
        self.movies_api = MoviesAPI(session)
