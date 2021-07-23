from src.rise.rise_connection import RiseConnection


class RiseCustomer:

    def __init__(self, rise_connection: RiseConnection):
        self.__connection = rise_connection

    def get(self, uid: str) -> dict:
        return self.__connection.make_request(
            'GET',
            f'/customers/{uid}'
        )

    def find(self, include_initiated=False, external_uid: str = None) -> list:
        return self.__connection.make_request(
            'GET',
            '/customers',
            params={
                'include_initiated': include_initiated,
                'external_uid': external_uid
            },
        )

    def update(self, uid: str, details: dict) -> dict:
        return self.__connection.make_request(
            'PUT',
            f'/customers/{uid}',
            body={
                'details': details
            },
        )

    def verify_identity(self, uid: str):
        return self.__connection.make_request(
            'PUT',
            f'/customers/{uid}/identity_verification',
        )
