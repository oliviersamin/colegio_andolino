from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):
    """ parent model """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    school_email = models.EmailField(blank=True, null=True)
    bank_account = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        ordering = ['user__last_name', 'user__first_name']
        verbose_name_plural = "Teachers"

    def __str__(self):
        displayed = "name: {}".format(self.user.get_full_name())
        return displayed

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def pupils(self):
        pupils = self.pupil.all()
        pupils = [pupil.last_name() + ' ' + pupil.first_name() for pupil in pupils]
        return ' - '.join(pupils)

    def display_user_details(self):
        return self.user.get_full_name()

    def teacher_id(self):
        return self.id
