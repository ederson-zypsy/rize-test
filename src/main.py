from src import params
from src.rise.rise_client import RiseClient
from src.rise.rise_connection import RiseConnection

rise_client = RiseClient(RiseConnection(params.PROGRAM_ID, params.HMAC_KEY))


def main(firstcard_user: dict):
    customer = get_or_create_customer(firstcard_user['firstcard_user_id'], firstcard_user['email'])
    while True:
        customer = get_custumer(customer['uid'])
        if customer['status'] == 'initiated':
            update_customer(customer['uid'], firstcard_user['details'])
            accept_customer_workflow_documents(customer)
            request_identity_verification(customer['uid'])
        elif customer['status'] == 'active':
            print('\nCustomer is activated!')
            return
        else:
            print(f'\nCustomer status: {customer["status"]}')


def get_or_create_customer(firstcard_user_id: str, firstcard_user_email: str) -> dict:
    print(f'\nFinding custumer with external uid = {firstcard_user_id}')
    customers = rise_client.customer.find(include_initiated=True, external_uid=firstcard_user_id)

    if customers['total_count'] == 0:
        print(f'Customer not found. Creating compliance workflow...')
        rise_client.compliance_workflow.create(firstcard_user_id, firstcard_user_email)
        customers = rise_client.customer.find(include_initiated=True, external_uid=firstcard_user_id)

    customer = customers['data'][0]
    print(f'uid: {customer["uid"]}\nstatus: {customer["status"]}\ntotal_balance: {customer["total_balance"]}')
    return customer


def get_custumer(uid: str) -> dict:
    return rise_client.customer.get(uid)


def update_customer(custumer_uid: str, details: dict):
    print(f'\nUpdating customer details')
    rise_client.customer.update(custumer_uid, details)


def accept_customer_workflow_documents(customer: dict):
    print('\nChecking customer workflow documents..')

    while True:
        compliance_workflow = rise_client.compliance_workflow.get_latest(customer["uid"])
        number_of_pending_documents = len(compliance_workflow["current_step_documents_pending"])
        if number_of_pending_documents == 0:
            print('All documents accepted')
            break

        print(
            f'Step {compliance_workflow["summary"]["current_step"]}: {number_of_pending_documents} pending documents')
        for pending_document in compliance_workflow['current_step_documents_pending']:
            print(f'Accepting document: {pending_document["name"]}')
            rise_client.compliance_workflow.acknowledge_document(
                uid=compliance_workflow['uid'],
                customer_uid=customer['uid'],
                document_uid=pending_document['uid'],
                accept=True,
                ip_address='189.37.71.51',
                user_name='User Name'
            )


def request_identity_verification(uid: str):
    print('\nRequesting for identity verification')
    rise_client.customer.verify_identity(uid)


if __name__ == "__main__":
    number = '16'
    main({
        'firstcard_user_id': f'firstcard-user-{number}',
        'email': f'edersonn@gmail.com{number}',
        'details': {
            'first_name': f'Ederson {number}',
            'middle_name': f'Machado {number}',
            'last_name': f'Lima {number}',
            # 'suffix': 'Jr.',
            'phone': f'555555{number.zfill(4)}',
            'ssn': f'111-22-{number.zfill(4)}',
            'dob': f'{number.zfill(4)}-12-08',
            'address': {
                'street1': '123 Abc St.',
                'street2': 'Apt 2',
                'city': 'Chicago',
                'state': 'IL',
                'postal_code': '12345',
            }
        }
    })
