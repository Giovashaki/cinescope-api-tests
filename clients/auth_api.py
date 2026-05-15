from clients.custom_requester import CustomRequester
from constants import AUTH_URL, LOGIN_ENDPOINT


class AuthAPI(CustomRequester):

    def __init__(self, session):
        super().__init__(session=session, base_url=AUTH_URL)

    def login_user(self, login_data, expected_status=200):
        return self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )

    def authenticate(self, email, password):
        login_data = {
            "email": email,
            "password": password
        }
        response = self.login_user(login_data).json()

        if "accessToken" not in response:
            raise KeyError("accessToken отсутствует в ответе")

        token = response["accessToken"]
        self._update_session_headers(**{"Authorization": f"Bearer {token}"})
