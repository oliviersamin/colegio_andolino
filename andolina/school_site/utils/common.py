import datetime
from django.db.models import Q
from v1.models import Child, Parent, Archive, Sheet, Activity


def get_user_activities(user, archive):
    pass


def get_all_family_activities(user):
    parent = Parent.objects.get(user=user)
    if parent.partner:
        pass


def get_dates_for_actual_school_year() -> list[dict]:
    """
    output: [{'month: 9, 'year': 2022}, {}...]
    """
    now = datetime.datetime.now()
    if now.month in range(9, 13):
        dates1 = [{'month': month,'year': now.year} for month in range(9, 13)]
        dates2 = [{'month': month, 'year': now.year + 1} for month in range(1, 7)]
        return dates1 + dates2
    elif now.month in range(1, 8):
        dates1 = [{'month': month,'year': now.year - 1} for month in range(9, 13)]
        dates2 = [{'month': month, 'year': now.year} for month in range(1, 7)]
        return dates1 + dates2


def get_data_for_month_year(user, month, year):
    """
    for a given user get all the activity for a given year and month
    return [
    {'user': <user_id>,
    'activities': [{
          'name': 'test',
          'payment': 'monthly',
          'price': 20,
          'sheet': {
              'year': '2022',
              'month': '11',
              'participation':[1, 7, 13, 24]
              }
          }
    ]
    },
    {}, ...
    ]

    """
    result = {'user': user, 'activities': []}
    # filters = Q(activity__users=user) & Q(is_archived=True) & Q(month=month) & Q(year=year)
    user_activities = user.activities.all()
    for activity in user_activities:
        res_activity = {}
        if activity.price_per_month:
            payment = 'monthly'
            price = activity.price_per_month
        elif activity.price_per_day:
            payment = 'daily'
            price = activity.price_per_day
        res_activity['payment'] = payment
        res_activity['price'] = price
        res_activity['name'] = activity.name
        research_filters = Q(is_archived=True) & Q(month=month) & Q(year=year)
        corresponding_sheet = activity.sheet.filter(research_filters).first()
        if corresponding_sheet:
            user_dates = from_sheet_content_to_user_participation(user, corresponding_sheet.content)
            res_activity['sheet'] = {'year': year, 'month': month, 'participation': user_dates}
            result['activities'].append(res_activity)
    return result


def from_sheet_content_to_user_participation(user: object, content: dict) -> list:
    """
    input: content = {'on': ['1_12', '1_16', '1_23', '4_12' ,'4_ 25', '<user_id>_day', ...]}
    output: days = [1, 8, 12, 14, 16, 23, 26, 30]
    """
    raw_data = content['on']
    return [item[item.find('_') + 1:] for item in raw_data if item.startswith(str(user.id) + '_')]


def get_data_for_actual_school_year(user):
    results = []
    dates_filter = get_dates_for_actual_school_year()
    for date in dates_filter:
        res = get_data_for_month_year(user, date['month'], date['year'])
        results.append(res)
    # filters = Q(activity__users=user) & Q(is_archived=True) & dates_filter
    # result['sheets'] = list(Sheet.objects.filter(filters))
    return results