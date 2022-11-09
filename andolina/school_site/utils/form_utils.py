from v1.models import Child, Group

PROFILE_FORM_FIELDS = [
    'first_name',
    'last_name',
    'email',
    'phone',
    'mobile',
    'address',
    'school_status',
    'school_email',
    'bank_account',
    'is_paying_bills',
]

MANY_TO_MANY_FIELDS = ['children', 'group']


def update_username_with_form(first_name: str, last_name: str) -> str:
    first_name = first_name.lower()
    last_name = last_name.lower()
    last_names = last_name.split(' ')
    username = [first_name] + last_names
    return '.'.join(username)


def set_initial_fields_profile_form(user: object, parent: object) -> dict:
    initial = {}
    for item in dir(parent):
        if item in PROFILE_FORM_FIELDS:
            initial[item] = getattr(parent, item)

    for item in dir(user):
        if item in PROFILE_FORM_FIELDS:
            initial[item] = getattr(user, item)

    for item in dir(parent):
        if item in MANY_TO_MANY_FIELDS:
            initial[item] = list(getattr(parent, item).all())
    return initial


def get_children_instance_from_form_field(data: list) -> list:
    res = [item.split(' ') for item in data]
    username = ['.'.join(item).lower() for item in res]
    return [Child.objects.get(user__username=item) for item in username]


def get_group_instance_from_form_field(data: list) -> list:
    return [Group.objects.get(name=item) for item in data]


def update_children_fields_profile_form(parent: object, field: str, new_data: list) -> None:
    current_data = list(getattr(parent, field).all())
    if current_data != new_data:
        [parent.children.remove(child) for child in current_data]
        [parent.children.add(child) for child in new_data]


def update_group_fields_profile_form(parent: object, field: str, new_data: list) -> None:
    current_data = list(getattr(parent, field).all())
    if current_data != new_data:
        [parent.group.remove(child) for child in current_data]
        [parent.group.add(child) for child in new_data]
