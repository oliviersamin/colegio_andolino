
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
    'operation': 'PUT',
    'data': {'username': 'user.test', 'password1': 'passwd_test', 'password2': 'passwd_test'}
}

# PUT CHILDREN
PUT_CHILDREN = {
    'model': 'Child',
    'operation': 'PUT',
    'data': {'user': 8, 'birth_date': "2015-10-27", 'age': 13, 'tutor': 1}
}

# PUT PARENTS
PUT_PARENTS = {
    'model': 'Parent',
    'operation': 'PUT',
    'data': {'user': 1, 'children': [1]}
}


# PUT TEACHERS
PUT_TEACHERS = {
    'model': 'Teacher',
    'operation': 'PUT',
    'data': {'user': 2, }
}


# PUT DOCUMENTS
PUT_DOCUMENTS = {
    'model': 'Document',
    'operation': 'PUT',
    'data': {'title': 'blabla', 'type': 'bill', 'recipient': 3, 'content': {'test': 'blab'}}
}


# PUT GROUPS
PUT_GROUPS = {
    'model': 'Group',
    'operation': 'PUT',
    'data': {'name': 'CdT', 'members': [1, 2], 'leader': 2, 'representative': 1}
}
