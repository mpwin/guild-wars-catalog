from django.db import models


class Release(models.Model):
    name = models.CharField(
        max_length=40,
        unique=True,
    )
    slug = models.SlugField(
        max_length=40,
        unique=True,
    )
    order = models.PositiveSmallIntegerField(
        unique=True,
    )

    def __str__(self):
        return self.name


class Map(models.Model):
    name = models.CharField(
        max_length=40,
        unique=True,
    )
    slug = models.SlugField(
        max_length=40,
        unique=True,
    )
    release = models.ForeignKey(
        Release,
        on_delete=models.PROTECT,
        related_name='maps',
    )
    order = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


class Collection(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20)
    note = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Skin(models.Model):
    api_id = models.PositiveIntegerField(primary_key=True)
    collection = models.ForeignKey(
        Collection,
        on_delete=models.SET_NULL,
        null=True,
        related_name='skins',
    )
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20)
    details = models.JSONField(default=dict)
    is_unlocked = models.BooleanField(default=False)

    def __str__(self):
        return self.name
