from django.db import models
from django.contrib.auth.models import User
import datetime
# from . import Parent, External
from v1.constants import PUBLIC_ACTIVITY
from school_site.constants import (
    PERMISSION_ACTIVITY_CHOICES,
)

PRICE_CHOICES = [('daily_price', 'daily price'), ('monthly_price', 'monthly price')]
# AWAITING_USERS = [('TEST', 'TEST')]


class Activity(models.Model):
    """ activity model """
    name = models.CharField(max_length=100, blank=False, null=True, help_text='name of the activity')
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='activity',
        help_text='Adult in charge',
        blank=True,
        null=True
    )
    users = models.ManyToManyField(User, related_name='activities', blank=True)
    nb_places_available = models.PositiveSmallIntegerField(blank=True, null=True)
    is_inscription_open = models.BooleanField(blank=True, null=True, default=True)
    is_all_year = models.BooleanField(blank=True, null=True, default=True)
    date = models.DateField(blank=True, null=True, help_text="date of the activity if it is not perform all year")
    days_hour = models.CharField(
        max_length=40,
        help_text="format: day1/start_hour-stop_hour, day2/hours example: Monday/15:30-16:30, Wednesday/15:30-16:30",
        blank=True,
        null=True)
    details = models.TextField(help_text="Explain to parents what is this activity", null=True, blank=True)
    price = models.CharField(max_length=40, choices=PRICE_CHOICES, blank=False, null=True, default='monthly_price')
    price_per_day = models.FloatField(blank=True, null=True)
    price_per_month = models.FloatField(blank=True, null=True)
    has_monthly_max_price = models.BooleanField(blank=True, null=True, default=False)
    max_price_per_month = models.FloatField(blank=True, null=True)
    money_earned_by_school = models.FloatField(blank=True, null=True)
    public = models.CharField(max_length=40, choices=PUBLIC_ACTIVITY, blank=False, null=True)
    comment_for_parent = models.TextField(blank=True, null=True)
    edit_permission = models.CharField(max_length=40, choices=PERMISSION_ACTIVITY_CHOICES, blank=True, null=True)
    ask_inscription = models.ManyToManyField(User, related_name='inscriptions', blank=True)

    class Meta:
        ordering = ['name', 'public', 'is_inscription_open']
        verbose_name_plural = "Activities"

    def __str__(self):
        return self.name

    def update_awaiting_users_list(self, user):
        """
        get the data and update the list to update the corresponding field
        """
        now = datetime.datetime.now()
        date_format = '%Y-%m-%d %H:%M:%S'
        displayed_data = user.get_full_name() + ' ' + datetime.datetime.strftime(now, date_format)
        return AWAITING_USERS.append((user.username, displayed_data))
