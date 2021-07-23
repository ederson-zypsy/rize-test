from typing import Optional

from src.rise.rise_connection import RiseConnection


class RiseComplianceWorkflow:

    def __init__(self, rise_connection: RiseConnection):
        self.__connection = rise_connection

    def create(self, customer_external_uid: str, email: str) -> dict:
        return self.__connection.make_request(
            'POST',
            '/compliance_workflows', body={
                'customer_external_uid': customer_external_uid,
                'email': email,
            }
        )

    def get_latest(self, customer_uid: str) -> dict:
        return self.__connection.make_request(
            'GET',
            f'/compliance_workflows/latest/{customer_uid}',
        )

    def acknowledge_document(self, uid: str, customer_uid: str, document_uid: str, accept: bool,
                             ip_address: Optional[str], user_name: Optional[str]) -> dict:
        return self.__connection.make_request(
            'PUT',
            f'/compliance_workflows/{uid}/acknowledge_document', body={
                'accept': 'yes' if accept else 'no',
                'customer_uid': customer_uid,
                'document_uid': document_uid,
                'ip_address': ip_address,
                'user_name': user_name,
            }
        )

    # TODO: method for endpoint "Acknowledge multiple Compliance Documents"
