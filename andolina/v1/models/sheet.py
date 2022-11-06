from django.db import models
from . import Activity

class Sheet(models.Model):
    """
    sheet model
    content looks like = {'on': [<button_name>, <button_name>,...]}
    """
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    year = models.CharField(max_length=4, blank=False, null=True)
    month = models.CharField(max_length=2, blank=False, null=True)
    content = models.JSONField()


    class Meta:
        ordering = ['activity', 'year', 'month']
        verbose_name_plural = "Sheets"

