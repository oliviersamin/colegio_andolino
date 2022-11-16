from django.db import models
from django.contrib.auth.models import User


class External(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True, blank=True)
    date_updated = models.DateField(auto_now=True, blank=True)

    class Meta:
        ordering = ['user__last_name', 'user__first_name']
        verbose_name_plural = "Externals"

    def __str__(self):
        return self.user.get_full_name()

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def external_id(self):
        return self.id

    def full_name(self):
        return self.user.get_full_name()

