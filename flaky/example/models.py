from django.db import models


class TheModel(models.Model):
    name = models.IntegerField()


class OrderedModel(models.Model):
    name = models.IntegerField()

    class Meta:
        ordering = ['name']
