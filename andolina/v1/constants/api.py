MODELS = ['User', 'Parent', 'Child', 'Teacher', 'Document', 'Group']
OPERATIONS_DB = ['POST', 'GET', 'PUT', 'DELETE']
OPERATIONS_LIST = ['POST', 'GET']
OPERATIONS_DETAILS = ['GET', 'PUT']

BASE_LOCAL_URL = 'http://localhost:8000/'
URI_USER_LIST = 'api/v1/users/'
URI_PARENT_LIST = 'api/v1/parents/'
URI_CHILD_LIST = 'api/v1/children/'
URI_TEACHER_LIST = 'api/v1/teachers/'
URI_DOCUMENT_LIST = 'api/v1/documents/'
URI_GROUP_LIST = 'api/v1/school_groups/'

HEADERS = {'Content-Type': 'application/json'}

ALL_URI = [
    URI_USER_LIST,
    URI_PARENT_LIST,
    URI_CHILD_LIST,
    URI_TEACHER_LIST,
    URI_DOCUMENT_LIST,
    URI_GROUP_LIST,
]

MAP_URI = {model: uri for model, uri in zip(MODELS, ALL_URI)}