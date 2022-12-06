from django import template
from django.contrib.auth.models import User
from v1.models import External, Parent, Child, Activity


register = template.Library()


def get_all_available_activities():
    return Activity.objects.filter(is_inscription_open=True)


register.filter('get_all_available_activities', get_all_available_activities)
