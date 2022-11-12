from django.db import models
from . import Activity

def get_year_choices():
    return [(item, str(item)) for item in range(2022, 2122)]


def get_month_choices():
    return [(item, str(item)) for item in range(1, 13)]


class Sheet(models.Model):
    """
    sheet model
    content looks like = {'on': [<button_name>, <button_name>,...]}
    """
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField(blank=True, null=True, choices=get_year_choices())
    month = models.PositiveSmallIntegerField(blank=True, null=True, choices=get_month_choices())
    content = models.JSONField()


    class Meta:
        ordering = ['activity', 'year', 'month']
        verbose_name_plural = "Sheets"

