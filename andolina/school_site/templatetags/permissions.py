from django import template
from django.contrib.auth.models import User
from v1.models import External


register = template.Library()


def is_external(user):
    return True if External.objects.filter(user__id=user.id).first() else False


register.filter('is_external', is_external)
