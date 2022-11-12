from django import template
from v1.models import Sheet


register = template.Library()


def sheet_exists(activity_id):
    """

    """
    sheets = Sheet.objects.filter(activity_id=activity_id)
    if sheets:
        return True
    return False


register.filter('sheet_exists', sheet_exists)
