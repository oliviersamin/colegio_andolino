from django.db import models
from django.contrib.auth.models import User
from v1.constants import (
    DOCUMENT_CREATION_TYPE,
    DOCUMENT_TYPE,
)


class Document(models.Model):
    """
    document model: The content is store as JSON. The idea underneath that is that all the documents will
    be generated automatically. A frame will be setup for each document and the key data will be insert into it.
    The content attribute will store only the key data to be abble to recreate the document if needed:
    Each type of Document will need specific JSON data into it.

    """
    title = models.CharField(max_length=50, blank=True, null=True)
    content = models.JSONField()
    created_by = models.OneToOneField(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    type = models.CharField(max_length=50, blank=True, null=True, choices=DOCUMENT_TYPE)
    type_creation = models.CharField(max_length=50, blank=True, null=True, choices=DOCUMENT_CREATION_TYPE)

    class Meta:
        ordering = ['title']
        verbose_name_plural = "Documents"

    def __str__(self):
        return self.title

    def creator(self):
        return self.created_by.user.get_full_name()
