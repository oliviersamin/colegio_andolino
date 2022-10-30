import requests
import json
import time
from andolina.v1.constants import (
    MODELS,
    OPERATIONS_DB,
    OPERATIONS_DETAILS,
    OPERATIONS_LIST,
    BASE_LOCAL_URL,
    HEADERS,
    MAP_URI,
    ALL_URI,
)
from samples_api_requests import (
    GET_USERS,
    GET_GROUPS,
    GET_PARENTS,
    GET_TEACHERS,
    GET_CHILDREN,
    GET_DOCUMENTS,
    POST_USERS,
    POST_PARENTS,
    POST_TEACHERS,
    POST_GROUPS,
    POST_DOCUMENTS,
    POST_CHILDREN,
)
"""
url = "https://127.0.0.1:8000/api/clients/"

payload = json.dumps({
  "first_name": "test_post",
  "last_name": "",
  "email": "email2@test.com",
  "phone": "",
  "mobile": "",
  "company_name": "",
  "date_created": "2021-11-29T11:40:01.863426Z",
  "date_updated": "2021-11-29T11:40:01.863458Z",
  "is_confirmed_client": False
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

"""


class Operation:
    """
    setup each CRUD operation on the databse with a kwarg as argument to run the appropriate method
    """
    def __init__(self, dict_operation: dict):
        """
        dict_operation contains all details on the operation to perform such as
        the model, the CRUD operation, the content of the data to post or put ...
        format is {'model': <model_name>, 'operation':<CRUD_operation_name>, 'data': <data>, 'model_id': <model_id>}
        """
        self.model = dict_operation['model']
        self.model_id = dict_operation['model_id'] if 'model_id' in dict_operation.keys() else ""
        self. operation = dict_operation['operation']
        self.data = json.dumps(dict_operation['data']) if 'data' in dict_operation.keys() else ""
        self.url = BASE_LOCAL_URL
        self.headers = HEADERS

    def verify_input(self):
        """
        Verify if model corresponds to existing one
        Verify if operation corresponds to existing one
        """
        if self.model  not in MODELS:
            error = 'ERROR - The possibles models are: \n' + ' - '.join(MODELS)
        elif self.operation not in OPERATIONS_DB:
            error = 'ERROR - The possibles operations are: \n' + ' - '.join(OPERATIONS_DB)
        else:
            error = ''
        return error

    def verify_data(self):
        """
        verify data for POST and PUT operation to use regarding each model
        """

    def set_uri(self):
        for key, value in MAP_URI.items():
            if self.model == key:
                if (self.operation in OPERATIONS_DETAILS) & (self.model_id):
                    self.url += value + str(self.model_id)
                elif (self.operation in OPERATIONS_LIST) & (not self.model_id):
                    self.url += value
                else:
                    pass # TODO: raise an Exception

    def execute(self):
        """
        perform the operation asked after verification that model and operation are correct type
        """
        if not self.verify_input():
            self.set_uri()
            if not self.data:
                return requests.request(self.operation, self.url, headers=self.headers)
            else:
                return requests.request(self.operation, self.url, headers=self.headers, data=self.data)
        else:
            return self.verify_input()


if __name__ == "__main__":
    # tests_GET = [GET_DOCUMENTS, GET_CHILDREN, GET_PARENTS, GET_TEACHERS, GET_GROUPS, GET_USERS]
    # tests_POST = [POST_CHILDREN, POST_DOCUMENTS, POST_GROUPS, POST_TEACHERS, POST_PARENTS, POST_USERS]
    tests_PUT = []
    for test in tests_PUT:
        print('-' * 50 + str(test) + '-' * 50)
        response = Operation(test).execute()
        print('response = ', response.content)
        time.sleep(2)
