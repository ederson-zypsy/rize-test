from src.rise.clients.rise_compliance_workflow import RiseComplianceWorkflow
from src.rise.clients.rise_customer import RiseCustomer
from src.rise.rise_connection import RiseConnection


class RiseClient:

    def __init__(self, rise_connection: RiseConnection):
        self.__rise_connection = rise_connection

        self.compliance_workflow = RiseComplianceWorkflow(self.__rise_connection)
        self.customer = RiseCustomer(self.__rise_connection)
        # TODO: add a client for all endpoints

