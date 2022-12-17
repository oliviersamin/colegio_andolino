from django.db import models
from django.contrib.auth.models import User
import datetime

LIMIT_CHOICES = [('minimum', 'minimum'), ('maximum', 'maximum')]

class Price(models.Model):
    """ price model """
    activity_to_limit = models.OneToOneField(
        'v1.Activity',
        on_delete=models.CASCADE,
        help_text='prices max or min',
        blank=True,
        null=True,
    )
    limit_type = models.CharField(max_length=40, choices=LIMIT_CHOICES, blank=False, null=True, default='maximum')
    value = models.FloatField(blank=False, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['activity_to_limit', 'date_created', 'date_updated', 'limit_type', 'value']
        verbose_name_plural = "Prices"
