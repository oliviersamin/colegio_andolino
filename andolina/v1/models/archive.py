from django.db import models
from django.contrib.auth.models import User
from . import Parent

YEAR_CHOICES = [(i, i) for i in range(2022, 2122)]
MONTH_CHOICES = [(i, i) for i in range(1, 13)]
TYPE_CHOICES = [('bill', 'bill'),]


class Archive(models.Model):
    """ archive model """
    name = models.CharField(max_length=100, blank=False, null=True, help_text='name of the activity')
    type = models.CharField(max_length=40, blank=True, null=True, choices=TYPE_CHOICES)
    year = models.PositiveSmallIntegerField(blank=True, null=True, choices=YEAR_CHOICES)
    month = models.PositiveSmallIntegerField(blank=True, null=True, choices=MONTH_CHOICES)
    sheets = models.ForeignKey('v1.Sheet', related_name='archive', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ['type', 'year', 'month', 'name']
        verbose_name_plural = "Archives"

    def __str__(self):
        return str(self.year) + '-' + str(self.month)
