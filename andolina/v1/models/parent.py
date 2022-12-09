from django.db import models
from django.contrib.auth.models import User
from .child import Child
from v1.constants.models import (
    SCHOOL_STATUS,
    SCHOOL_GROUPS,
)


class Parent(models.Model):
    """ parent model """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    partner = models.ForeignKey('v1.Parent', on_delete=models.CASCADE, help_text='wife/husband of the user', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    children = models.ManyToManyField(Child, blank=True, related_name='parent')
    school_status = models.CharField(max_length=20, blank=True, null=True, choices=SCHOOL_STATUS)
    # groups = models.CharField(max_length=20, blank=True, null=True, choices=SCHOOL_GROUPS)
    school_email = models.EmailField(blank=True, null=True)
    nif = models.CharField(max_length=20, blank=True, null=True)
    bank_account = models.CharField(max_length=20, blank=True, null=True)
    is_paying_bills = models.BooleanField(blank=True, null=True, default=False)
    date_start_school = models.DateField(blank=True, null=True)
    date_stop_school = models.DateField(blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['user__last_name', 'user__first_name']
        verbose_name_plural = "Parents"

    def __str__(self):
        return self.user.get_full_name()

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def parent_id(self):
        return self.id

    def child(self):
        children = [child.last_name() + ' ' + child.first_name() for child in self.children.all()]
        return ' - '.join(children)

    def groups(self):
        groups = [group.name for group in self.group.all()]
        return ' - '.join(groups)