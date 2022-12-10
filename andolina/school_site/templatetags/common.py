from django import template
from django.contrib.auth.models import User
from v1.models import External, Parent, Child, Activity


register = template.Library()


@register.simple_tag
def get_all_activities_with_inscription_opened():
    return Activity.objects.filter(is_inscription_open=True)


@register.simple_tag
def is_family_member_into_a_waiting_list(family, activity_id):
    results = []
    for category, users in family.items():
        for user in users:
            if user.user.inscriptions.filter(id=activity_id).first():
                results.append(user.user)
    return results


@register.simple_tag
def is_user_into_waiting_list(user, activity_id):
    if user.user.inscriptions.filter(id=activity_id).first():
        return True
    return False


@register.simple_tag
def users_to_be_added(family, activity_id):
    into_list = []
    result = []
    public = ''
    for category, members in family.items():
        for member in members:
            if member.user in Activity.objects.get(id=activity_id).ask_inscription.all():
                into_list.append(member.user)
                public = category
    if public == '':
        return True
    else:
        for category, members in family.items():
            if category == public:
                for member in members:
                    if member.user not in into_list:
                        return True
    return False


@register.simple_tag
def is_family_member_into_an_activity():
    return Activity.objects.filter(is_inscription_open=True)
