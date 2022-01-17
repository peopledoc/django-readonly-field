from django.db import models


class Car(models.Model):

    wheel_number = models.IntegerField()
    manufacturer = models.CharField(max_length=100)

    def __str__(self):
        return "{car.manufacturer} Car with {car.wheel_number} wheels".format(
            car=self)

    class ReadonlyMeta:
        readonly = ["manufacturer"]


class Book(models.Model):
    """
    A completely different model
    """
    ref = models.IntegerField()
    iban = models.CharField(max_length=100)
    name = models.CharField(max_length=250)

    def __str__(self):
        return "{book.name} (ref: {book.ref}, iban: {book.iban})"

    class ReadonlyMeta:
        readonly = ["ref", "iban"]


class Bus(models.Model):
    """
    This is the same model as Car but with readonly fields the other way
    around to make sure we don't mix them up.
    """

    wheel_number = models.IntegerField()
    manufacturer = models.CharField(max_length=100)

    def __str__(self):
        return "{car.manufacturer} Bus with {car.wheel_number} wheels".format(
            car=self)

    class ReadonlyMeta:
        readonly = ["wheel_number"]
