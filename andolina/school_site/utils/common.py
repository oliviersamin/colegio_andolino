import datetime
from django.db.models import Q
from v1.models import Child, Parent, Archive, Sheet, Activity


def get_user_activities(user, archive):
    pass


def get_all_family_activities(user):
    parent = Parent.objects.get(user=user)
    if parent.partner:
        pass


def get_activities_for_actual_school_year(user):
    """
    1. get the dates (year and month) for whole school year
    2. get related activities with sheet archived
    """
    now = datetime.datetime.now()
    if now.month in range(9, 13):
        dates_filters = (Q(year=now.year) & Q(month__in=list(range(9, 13)))) | (
                Q(year=now.year + 1) & Q(month__in=list(range(1, 7))))
    else:
        dates_filters = (Q(year=now.year - 1) & Q(month__in=list(range(9, 13)))) | (
                Q(year=now.year) & Q(month__in=list(range(1, 7))))
    activities = user.activities.all()
    return [activity for activity in activities if activity.sheet.all().filter(dates_filters)]

