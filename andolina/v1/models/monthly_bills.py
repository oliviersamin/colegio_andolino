from django.db import models
from django.contrib.auth.models import User
import datetime


class MonthlyBills(models.Model):
    """ activity monthly bills to be accessed only by person in charge of communicating bills to bank """
    date = models.DateField(blank=False, null=True, help_text='monthly bill')
    data = models.JSONField(blank=True, null=True, help_text="ex: {'2022_12': {'child1': 300, 'child2': 200 ...}}")

    class Meta:
        ordering = ['date']
        verbose_name_plural = "Monthly bills"

    def __str__(self):
        return self.name

