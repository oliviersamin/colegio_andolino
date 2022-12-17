from django.db import models
from django.contrib.auth.models import User
import datetime

LIMIT_CHOICES = [('minimum', 'minimum'), ('maximum', 'maximum')]

class Price(models.Model):
    """ price model """
    activity = models.ForeignKey(
        'v1.Activity',
        on_delete=models.CASCADE,
        related_name='price_limitation',
        help_text='prices max or min',
        blank=True,
        null=True,
        unique=True,
    )
    limit_type = models.CharField(max_length=40, choices=LIMIT_CHOICES, blank=False, null=True, default='maximum')
    value = models.FloatField(blank=False, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['activity', 'date_created', 'date_updated', 'limit_typa', 'value']
        verbose_name_plural = "Prices"
