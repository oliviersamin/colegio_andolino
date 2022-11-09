from django.db import models
from django.contrib.auth.models import User
import datetime
from .teacher import Teacher

class Child(models.Model):
    """ parent model """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField()
    age = models.IntegerField(blank=True, null=True)
    tutor = models.ForeignKey(Teacher, related_name='pupil', on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True, blank=True)
    date_updated = models.DateField(auto_now=True, blank=True)

    class Meta:
        ordering = ['user__last_name', 'user__first_name']
        verbose_name_plural = "Children"

    def __str__(self):
        return self.user.get_full_name()

    def get_age(self):
        delta = (datetime.date.today() - self.birth_date).days
        self.age = int(delta/365.25)
        return self.age

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def parents(self):
        parents = self.parent.all()
        parents = [parent.last_name() + ' ' + parent.first_name() for parent in parents]
        return ' - '.join(parents)

    def display_user_details(self):
        return self.user.get_full_name()

    def child_id(self):
        return self.id
