from django.core.management.base import BaseCommand, CommandError
import requests
import json
import time
from django.db.models import Q
from django.contrib.auth.models import User
from v1.constants import (
    MODELS,
    OPERATIONS_DB,
    OPERATIONS_DETAILS,
    OPERATIONS_LIST,
    BASE_LOCAL_URL,
    HEADERS,
    MAP_URI,
    ALL_URI,
)
from v1.utils import (
    GET_USERS,
    GET_GROUPS,
    GET_PARENTS,
    GET_TEACHERS,
    GET_CHILDREN,
    GET_DOCUMENTS,
    CYCLE_USER,
)
from v1.models import (
    Parent,
    Child,
    Teacher,
    Group,
    Document
)


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
            # TODO: Raise error
            error = 'ERROR - The possibles operations are: \n' + ' - '.join(OPERATIONS_DB)
        else:
            # TODO: Raise error
            error = ''
        return error

    def is_performed(self, model_id='') -> str:
        """
        if method is not 'GET' check with that the operation has been performed successfully
        """
        if self.operation == 'POST':
            try:
                verification = eval(self.model).objects.get(username=json.loads(self.data)['username'])
                return str(verification.id)
            except Exception as e:
                print(e)
                return ''

        elif self.operation == 'PUT':
            try:
                verification = eval(self.model).objects.get(id=json.loads(self.data)['id'])
                return str(verification.id)
            except Exception as e:
                print(e)
                return ''
        elif self.operation == 'DELETE':
            pass

        # TODO: check operation with django query regarding id or data or count of items


    def set_uri(self):
        for key, value in MAP_URI.items():
            if self.model == key:
                if (self.operation in OPERATIONS_DETAILS) & (self.model_id != ''):
                    self.url += value + str(self.model_id) + '/'
                elif (self.operation in OPERATIONS_LIST) & (not self.model_id != ''):
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


class Command(BaseCommand):
    help = 'Operations  verification on DB'

    def add_arguments(self, parser):
        pass

    def check_post(self):
        start_users = User.objects.all().count()
        operation = Operation(CYCLE_USER['POST'])
        response = operation.execute()
        time.sleep(2)
        print('code_response = ', response.status_code)
        print('response = ', response.content)
        if operation.is_performed():
            return True
        return False

    def check_operations(self):
        tests_GET = [GET_DOCUMENTS, GET_CHILDREN, GET_PARENTS, GET_TEACHERS, GET_GROUPS, GET_USERS]
        tests_POST = [POST_CHILDREN, POST_DOCUMENTS, POST_GROUPS, POST_TEACHERS, POST_PARENTS, POST_USERS]
        tests_PUT = [PUT_GROUPS, PUT_DOCUMENTS, PUT_TEACHERS, PUT_PARENTS, PUT_USERS, PUT_CHILDREN]
        tests_DELETE = [DELETE_GROUPS, DELETE_USERS, DELETE_CHILDREN, DELETE_PARENTS, DELETE_TEACHERS, DELETE_DOCUMENTS]
        tests_OPERATION = [tests_PUT, tests_GET, tests_POST, tests_DELETE]
        for test in tests_OPERATION:
            print('-' * 50 + str(test) + '-' * 50)
            response = Operation(test).execute()
            print('code_response = ', response.status_code)
            print('response = ', response.content)
            time.sleep(2)

    def handle(self, *args, **options):
        check_operations()