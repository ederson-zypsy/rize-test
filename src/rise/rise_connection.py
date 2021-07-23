from datetime import datetime
from typing import Optional

import jwt
import requests


class RiseConnection:
    # TODO: parameter for environment (sandbox, integration, validation, production)
    BASE_URL = 'https://sandbox.rizefs.com/api/v1'

    def __init__(self, program_id, hmac_key):
        self.__program_id = program_id
        self.__hmac_key = hmac_key
        self.__token__ = self.__new_token()

    def make_request(self, http_operation: str, path: str, params: Optional[dict] = None, body: Optional[dict] = None):
        response = requests.request(
            http_operation,
            self.BASE_URL + path,
            headers={
                'Accept': 'application/json',
                "Content-Type": "application/json",
                # TODO: verify token expiration and refresh token
                'Authorization': self.__token__
            },
            params=params,
            json=body
        )
        if response.ok:
            return response.json()
        # TODO: improve error handling
        raise Exception(f'Error while calling endpoint: {path}: status: {response.status_code}, text: {response.text}')

    def __new_token(self):
        encoded_jwt = jwt.encode({
            "iat": datetime.timestamp(datetime.now()),
            "sub": self.__program_id
        }, self.__hmac_key, algorithm="HS512")
        response = requests.post(self.BASE_URL + "/auth",
                                 headers={"Accept": "application/json", 'Authorization': encoded_jwt})
        if response.ok:
            return response.json()['token']
        # TODO: improve error handling
        raise Exception('Error while getting token: ' + response.text)
