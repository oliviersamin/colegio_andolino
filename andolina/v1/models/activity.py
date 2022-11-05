from django.db import models
from . import Parent

class Activity(models.Model):
    """ activity model """
    name = models.CharField(max_length=100, blank=False, null=True, help_text='name of the activity')
    creator = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='activity', help_text='Parent in charge')
    is_all_year = models.BooleanField(blank=True, null=True)
    price_per_day = models.FloatField(blank=True, null=True)
    price_per_month = models.FloatField(blank=True, null=True)
    is_for_children = models.BooleanField(blank=True, null=True)
    is_for_parents = models.BooleanField(blank=True, null=True)
    money_earned_by_school = models.FloatField(blank=True, null=True)
    date = models.DateField(blank=True, null=True, help_text="date of the activity if it is not perform all year")

    class Meta:
        ordering = ['name', 'creator']
        verbose_name_plural = "Activities"

