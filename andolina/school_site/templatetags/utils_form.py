import datetime
from django.db.models import Q
from django import template
from v1.models import Child, Parent, Activity, Sheet, Archive


register = template.Library()


# my activities page buttons
def sheet_to_display(activity_id):
    """
    """
    sheets = Sheet.objects.filter(activity_id=activity_id).filter(is_archived=False)
    if sheets:
        return True
    return False


def are_all_sheets_created(sheets) -> bool:
    """
    1. filter all existing sheets for the activity with correct dates
    2. is len(sheets) == 10?
        if yes no create more sheet --> True
        if no create only the missing sheets -> return False

    """
    now = datetime.datetime.now()
    if now.month in range(9, 13):
        dates_filters = (Q(year=now.year) & Q(month__in=list(range(9, 13)))) | (
                Q(year=now.year + 1) & Q(month__in=list(range(1, 7))))
    else:
        dates_filters = (Q(year=now.year - 1) & Q(month__in=list(range(9, 13)))) | (
                Q(year=now.year) & Q(month__in=list(range(1, 7))))
    if len(sheets.filter(dates_filters)) == 10:
        return True
    return False


def is_checkbutton_selected(button_name, selected_buttons):
    if selected_buttons:
        if button_name in selected_buttons['on']:
            return True
        return False
    return False


def is_public_children(public):
    if public == 'children':
        return True
    return False


def is_selected_user(user: object, activity: object) -> bool:
    if activity.public == 'children':
        users = [Child.objects.get(user=user) for user in activity.users.all()]
    else:
        users = [Parent.objects.get(user=user) for user in activity.users.all()]

    if user in users:
        return True
    return False


def is_inscription_open(activity: object):
    if activity.is_inscription_open:
        return True
    return False


def get_past_or_present_sheets(activity_id):
    general_filters = (Q(activity_id=activity_id) & Q(is_archived=False))
    now = datetime.datetime.now()
    dates_filters = (Q(year=now.year) & Q(month__lte=now.month))
    filters = dates_filters & general_filters
    # sheets = Sheet.objects.filter(filters)
    sheets = Sheet.objects.filter(activity_id=activity_id).filter(month__lte=now.month).filter(year=now.year).filter(is_archived=False)
    return sheets


def is_past_or_present_sheet(activity_id):
    sheets = get_past_or_present_sheets(activity_id)
    if sheets:
        return True
    return False


def is_oldest_sheet(activity_id):
    return get_past_or_present_sheets(activity_id)[0].id


register.filter('is_oldest_sheet', is_oldest_sheet)
register.filter('is_past_or_present_sheet', is_past_or_present_sheet)
register.filter('are_all_sheets_created', are_all_sheets_created)
register.filter('is_inscription_open', is_inscription_open)
register.filter('sheet_to_display', sheet_to_display)
register.filter('is_checkbutton_selected', is_checkbutton_selected)
register.filter('is_public_children', is_public_children)
register.filter('is_selected_user', is_selected_user)
