from django import template
from v1.models import Sheet


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

register.filter('sheet_exists', sheet_exists)
register.filter('is_checkbutton_selected', is_checkbutton_selected)
