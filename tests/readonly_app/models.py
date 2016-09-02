from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Car(models.Model):

    wheel_number = models.IntegerField()
    manufacturer = models.CharField(max_length=100)

    def __str__(self):
        return "{car.manufacturer} Car with {car.wheel_number} wheels".format(
            car=self)

    class ReadOnlyMeta:
        read_only = ["manufacturer"]


@python_2_unicode_compatible
class Book(models.Model):

    ref = models.IntegerField()
    iban = models.CharField(max_length=100)
    name = models.CharField(max_length=250)

    class ReadOnlyMeta:
        read_only = ["ref", "iban"]

