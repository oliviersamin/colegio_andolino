from django.db import models
from django.contrib.auth.models import User
# from . import Parent, External
from v1.constants import PUBLIC_ACTIVITY
from school_site.constants import PERMISSION_ACTIVITY_CHOICES


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
    price_per_day = models.FloatField(blank=True, null=True)
    price_per_month = models.FloatField(blank=True, null=True)
    money_earned_by_school = models.FloatField(blank=True, null=True)
    public = models.CharField(max_length=40, choices=PUBLIC_ACTIVITY, blank=False, null=True)
    comment_for_parent = models.TextField(blank=True, null=True)
    edit_permission = models.CharField(max_length=40, choices=PERMISSION_ACTIVITY_CHOICES, blank=True, null=True)

    class Meta:
        ordering = ['name', 'public', 'is_inscription_open']
        verbose_name_plural = "Activities"

    def __str__(self):
        return self.name