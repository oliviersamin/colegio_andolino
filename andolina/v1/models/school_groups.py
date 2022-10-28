from django.db import models
from v1.constants.models import (
    SCHOOL_GROUPS,
)
from .parent import Parent

class Group(models.Model):
    """ parent model """
    members = models.ManyToManyField(Parent, related_name='members')
    name = models.CharField(max_length=20, blank=True, null=True, choices=SCHOOL_GROUPS)
    representative = models.ForeignKey(Parent, related_name='group_rep', on_delete=models.CASCADE)
    leader = models.ForeignKey(Parent, related_name='group_leader', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Groups"

    def __str__(self):
        return self.name

    def representative_name(self):
        return self.representative.user.get_full_name()

    def leader_name(self):
        return self.leader.user.get_full_name()

    def group_members(self):
        members = [member.last_name() + ' ' + member.first_name() for member in self.members.all()]
        return ' - '.join(members)

    def group_id(self):
        return self.id
