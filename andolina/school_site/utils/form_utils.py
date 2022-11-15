from v1.models import Child, Group, Parent
import datetime
from django.contrib.auth.models import User
from v1.models import Child, Sheet
import calendar


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

USER_FORM_FIELD = [
    'first_name',
    'last_name',

]

CHILD_FORM_FIELD = ['birth_date',]

ACTIVITY_FORM_FIELDS = [
    'name',
    'is_all_year',
    'price_per_day',
    'price_per_month',
    'public',
    'comment_for_parent',
    'money_earned_by_school',
    'date',
    'is_inscription_open',
    'nb_places_available'
]

SHEET_FORM_FIELDS = ['year', 'month', 'content']

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


def get_parents_instance_from_form_field(data: list):
    res = [item.split(' ') for item in data]
    username = ['.'.join(item).lower() for item in res]
    return [Parent.objects.get(user__username=item) for item in username]


def set_initial_child_fields(child):
    initial = {}
    for item in dir(child):
        if item in USER_FORM_FIELD:
            initial[item] = getattr(child.user, item)
        elif item in CHILD_FORM_FIELD:
            initial[item] = getattr(child, item)
    return initial


def set_initial_activity_fields(activity: object) -> dict:
    initial = {}
    for item in dir(activity):
        if item in ACTIVITY_FORM_FIELDS:
            initial[item] = getattr(activity, item)
    return initial


def save_activity_form_fields(form, activity: object) -> None:
    for item in dir(activity):
        if item in ACTIVITY_FORM_FIELDS:
            setattr(activity, item, form.cleaned_data[item])
        activity.save()


def create_user_from_child_form(form: object) -> None:
    new_user = User()
    last_names = form.cleaned_data['last_name'].split(' ')
    username = [form.cleaned_data['first_name']] + last_names
    username = '.'.join(username).lower()
    new_user.username = username
    new_user.first_name = form.cleaned_data['first_name']
    new_user.last_name = form.cleaned_data['last_name']
    new_user.save()
    return new_user


def create_child_from_new_user(form, user):
    new_child = Child()
    new_child.user_id = User.objects.get(username=user.username).id
    new_child.birth_date = form.cleaned_data['birth_date']
    now = datetime.datetime.now()
    now = datetime.date(now.year, now.month, now.day)
    age = (now - new_child.birth_date).days
    age = int(age / 365.25)
    new_child.age = age
    new_child.save()
    return new_child


def users_and_dates_for_sheet_table(sheet_id: int) -> dict:
    sheet = Sheet.objects.get(id=sheet_id)
    users = User.objects.filter(activities=sheet.activity)
    headers_column = get_current_month_dates_headers()
    rows = [{
        'label': user.get_full_name(),
        'content': [str(user.id) + '_' + str(i) for i in range(1, len(headers_column['header_days']) + 1)]}
        for user in users]
    return headers_column, rows


def get_current_month_dates_headers() -> dict:
    now = datetime.datetime.now()
    raw = calendar.month(now.year, now.month)
    raw_splited = raw.split('\n')[1:]
    raw_splited_cleaned = [line.split(' ') for line in raw_splited]
    calendar_sheet = [[char for char in line if char] for line in raw_splited_cleaned]
    calendar_sheet = [line for line in calendar_sheet if line]
    index = int(calendar_sheet[1][-1])
    # first_day = calendar_sheet[0][-index]
    first_week = calendar_sheet[0][-index:]
    nb_days = int(calendar_sheet[-1][-1])
    days = first_week + calendar_sheet[0] * 6
    header_days = days[:nb_days]
    header_numbers = list(range(1, nb_days + 1))
    return {'header_days': header_days, 'header_numbers': header_numbers}


def set_initial_sheet_fields(sheet: object) -> dict:
    initial = {}
    for item in dir(sheet):
        if item in SHEET_FORM_FIELDS:
            initial[item] = getattr(sheet, item)
    return initial
