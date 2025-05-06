from django.db import models


class Skin(models.Model):
    api_id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20)
    details = models.JSONField(default=dict)
