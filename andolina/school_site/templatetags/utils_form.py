import datetime

from django import template
from v1.models import Child, Parent, Activity, Sheet, Archive


register = template.Library()


# my activities page buttons
def sheet_exists(activity_id):
    """
    """
    sheets = Sheet.objects.filter(activity_id=activity_id)
    now = datetime.datetime.now()
    if sheets:
        sheet = [sheet for sheet in sheets if (sheet.year == now.year) & (sheet.month == now.month)][0]
        if sheet and not sheet.is_archived:
            return True
    return False


def is_monthly_sheet_archived(sheet_id):
    """
    1. archive
    2. one sheet existing for this activity and archive?
    """
    now = datetime.datetime.now()
    archive = Archive.objects.filter(year=now.year).filter(month=now.month).first()
    if archive:
        if sheet_id:
            sheet = Sheet.objects.get(id=sheet_id)
            if (sheet.year == now.year) & (sheet.month == now.month) & (sheet.is_archived):
                return True
        return False
    archive = Archive()
    archive.year = now.year
    archive.month = now.month
    archive.save()
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


register.filter('is_monthly_sheet_archived', is_monthly_sheet_archived)
register.filter('is_inscription_open', is_inscription_open)
register.filter('sheet_exists', sheet_exists)
register.filter('is_checkbutton_selected', is_checkbutton_selected)
register.filter('is_public_children', is_public_children)
register.filter('is_selected_user', is_selected_user)
