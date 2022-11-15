from django import template
from v1.models import Child, Parent, Activity, Sheet


register = template.Library()


# my activities page buttons
def sheet_exists(activity_id):
    """

    """
    sheets = Sheet.objects.filter(activity_id=activity_id)
    if sheets:
        return True
    return False


def is_checkbutton_selected(button_name, selected_buttons):
    if button_name in selected_buttons['on']:
        return True
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


register.filter('sheet_exists', sheet_exists)
register.filter('is_checkbutton_selected', is_checkbutton_selected)
register.filter('is_public_children', is_public_children)
register.filter('is_selected_user', is_selected_user)
