
########################################### GET ###################################################

# GET USERS
GET_USERS = {
    'model': 'User',
    'operation': 'GET'
}
# GET PARENTS
GET_PARENTS = {
    'model': 'Parent',
    'operation': 'GET'
}
# GET CHILDREN
GET_CHILDREN = {
    'model': 'Child',
    'operation': 'GET'
}
# GET TEACHERS
GET_TEACHERS = {
    'model': 'Teacher',
    'operation': 'GET'
}
# GET DOCUMENTS
GET_DOCUMENTS = {
    'model': 'Document',
    'operation': 'GET'
}
# GET GROUPS
GET_GROUPS = {
    'model': 'Group',
    'operation': 'GET'
}

########################################### POST ###################################################

# POST USERS
POST_USERS = {
    'model': 'User',
    'operation': 'POST',
    'data': {'username': 'user.test', 'password1': 'passwd_test', 'password2': 'passwd_test'}
}

# POST CHILDREN
POST_CHILDREN = {
    'model': 'Child',
    'operation': 'POST',
    'data': {'user': 8, 'birth_date': "2015-10-27", 'age': 13, 'tutor': 1}
}

# POST PARENTS
POST_PARENTS = {
    'model': 'Parent',
    'operation': 'POST',
    'data': {'user': 1, 'children': [1]}
}


# POST TEACHERS
POST_TEACHERS = {
    'model': 'Teacher',
    'operation': 'POST',
    'data': {'user': 2, }
}


# POST DOCUMENTS
POST_DOCUMENTS = {
    'model': 'Document',
    'operation': 'POST',
    'data': {'title': 'blabla', 'type': 'bill', 'recipient': 3, 'content': {'test': 'blab'}}
}


# POST GROUPS
POST_GROUPS = {
    'model': 'Group',
    'operation': 'POST',
    'data': {'name': 'CdT', 'members': [1, 2], 'leader': 2, 'representative': 1}
}

########################################### PUT ###################################################

# PUT USERS
PUT_USERS = {
    'model': 'User',
    'model_id': 9,
    'operation': 'PUT',
    'data': {'username': 'user.test.put', 'first_name': 'user', 'last_name': 'test_put', 'groups': [1], 'is_staff': True, 'is_active': True, 'is_superuser': False}
}

# PUT CHILDREN
PUT_CHILDREN = {
    'model': 'Child',
    'model_id': 9,
    'operation': 'PUT',
    'data': {'user': 9, 'birth_date': "1915-10-27", 'age': 108, 'tutor': 2}
}

# PUT PARENTS
PUT_PARENTS = {
    'model': 'Parent',
    'model_id': 1,
    'operation': 'PUT',
    'data': {'user': 9, 'children': [9], 'groups': 4}
}


# PUT TEACHERS
PUT_TEACHERS = {
    'model': 'Teacher',
    'model_id': 1,
    'operation': 'PUT',
    'data': {'user': 9, 'phone': '666666666'}
}


# PUT DOCUMENTS
PUT_DOCUMENTS = {
    'model': 'Document',
    'model_id': 1,
    'operation': 'PUT',
    'data': {'title': 'test_put', 'type': 'bill', 'recipient': 9, 'content': {'test_put': 'blab_put'}, 'type_creation': 'auto'}
}

# PUT GROUPS
PUT_GROUPS = {
    'model': 'Group',
    'model_id': 3,
    'operation': 'PUT',
    'data': {'name': 'CdT', 'members': [1, 2], 'leader': 2, 'representative': 1}
}

########################################### DELETE ###################################################

# DELETE USERS
DELETE_USERS = {
    'model': 'User',
    'model_id': 11,
    'operation': 'DELETE',
    'data': {}
}

# DELETE CHILDREN
DELETE_CHILDREN = {
    'model': 'Child',
    'model_id': 10,
    'operation': 'DELETE',
    'data': {}
}

# DELETE PARENTS
DELETE_PARENTS = {
    'model': 'Parent',
    'model_id': 41,
    'operation': 'DELETE',
    'data': {}
}


# DELETE TEACHERS
DELETE_TEACHERS = {
    'model': 'Teacher',
    'model_id': 1,
    'operation': 'DELETE',
    'data': {}
}


# DELETE DOCUMENTS
DELETE_DOCUMENTS = {
    'model': 'Document',
    'model_id': 29,
    'operation': 'DELETE',
    'data': {}
}

# DELETE GROUPS
DELETE_GROUPS = {
    'model': 'Group',
    'model_id': 3,
    'operation': 'DELETE',
    'data': {}
}
