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
