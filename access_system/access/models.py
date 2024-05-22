import itertools
import bcrypt

from django.db import models
from django.conf import settings


class Source(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "source"


class UserSource(models.Model):
    source = models.ForeignKey("Source", on_delete=models.PROTECT, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = "user_source"


class AccessHistory(models.Model):
    source = models.ForeignKey("Source", on_delete=models.PROTECT, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)
    hasAccess = models.BooleanField()
    access_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "access_history"


class Operation(models.Model):
    done = models.BooleanField(default=False)
    result = models.JSONField(default=dict)

    class Meta:
        db_table = "operation"