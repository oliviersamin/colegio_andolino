import requests
import json
from v1.constants import (
    MODELS,
    OPERATIONS_DB,
    BASE_LOCAL_URL,
    URI_PARENT_LIST,
    URI_DOCUMENT_LIST,
    URI_TEACHER_LIST,
    URI_CHILD_LIST,
    URI_GROUP_LIST,
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
        format is {'model': <model_name>, 'operation':<CRUD_operation_name>, 'data': <data>}
        """
        self.model = dict_operation['model']
        self. operation = dict_operation['operation']
        self.data = dict_operation['data']

    def __create(self):
        pass

    def __read(self):
        pass

    def __update(self):
        pass

    def __delete(self):
        pass

    def execute(self):
        """
        perform the operation asked after verififcation that model and operation are correct type
        """
