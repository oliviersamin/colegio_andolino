from v1.models import Child, Parent, Archive, Sheet, Activity


def get_user_activities(user, archive):
    pass


def get_all_family_activities(user):
    parent = Parent.objects.get(user=user)
    if parent.partner:
        pass
