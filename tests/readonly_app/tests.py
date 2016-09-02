from contextlib import contextmanager

from django.test import TestCase
from django.db import connection
from django.test.utils import CaptureQueriesContext

# Create your tests here.
from .models import Car


class ReadOnlyFieldTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.peugeot_car = Car.objects.create(wheel_number=5)
        connection.cursor().execute(
            "UPDATE readonly_app_car "
            "SET manufacturer='Peugeot' WHERE id=%s",
            [cls.peugeot_car.id])

    def setUp(self):
        self.peugeot_car.refresh_from_db()

    @contextmanager
    def assertSQLQueries(self):
        """
        Asserts that the SQL from the queries don't mention
        the read_only field. SELECTS are authorized, though.
        """
        with CaptureQueriesContext(connection=connection) as capture:
            yield

        for query in capture.captured_queries:
            if not query['sql'].startswith("SELECT"):
                self.assertNotIn("manufacturer", query['sql'])

    def test_create(self):
        with self.assertSQLQueries():
            car = Car.objects.create(wheel_number=4)

        car.refresh_from_db()

        self.assertEqual(car.manufacturer, "Renault")

        with self.assertSQLQueries():
            car = Car.objects.create(manufacturer="Honda", wheel_number=3)

        car.refresh_from_db()
        self.assertEqual(car.manufacturer, "Renault")

    def test_save(self):
        with self.assertSQLQueries():
            car = Car(wheel_number=3)
            car.save()

        car.refresh_from_db()

        self.assertEqual(car.manufacturer, "Renault")

        with self.assertSQLQueries():
            car = Car(wheel_number=3, manufacturer="Opel")
            car.save()

        car.refresh_from_db()
        self.assertEqual(car.manufacturer, "Renault")

    def test_save_update(self):
        car = self.peugeot_car

        with self.assertSQLQueries():
            car.save()

        car.refresh_from_db()
        self.assertEqual(car.manufacturer, "Peugeot")

        with self.assertSQLQueries():
            car.wheel_number = 7
            car.save()

        car.refresh_from_db()
        self.assertEqual(car.manufacturer, "Peugeot")

        with self.assertSQLQueries():
            car.manufacturer = "Citroen"
            car.save()

        car.refresh_from_db()
        self.assertEqual(car.manufacturer, "Peugeot")

    def test_update(self):
        car = self.peugeot_car
        with self.assertSQLQueries():
            Car.objects.filter(pk=car.pk).update(wheel_number=12)

        car.refresh_from_db()
        self.assertEqual(car.manufacturer, "Peugeot")

        with self.assertSQLQueries():
            Car.objects.filter(pk=car.pk).update(manufacturer="Ferrari")

        car.refresh_from_db()
        self.assertEqual(car.manufacturer, "Peugeot")

    def test_get_or_create(self):

        #Here, the query contains
        car, __ = Car.objects.get_or_create(wheel_number=3)

        car.refresh_from_db()
        self.assertEqual(car.manufacturer, "Renault")

        with self.assertSQLQueries():
            car, __ = Car.objects.get_or_create(
                wheel_number=3,
                defaults={"manufacturer": "Volkswagen"})

        car.refresh_from_db()
        self.assertEqual(car.manufacturer, "Renault")

    def test_bulk_create(self):

        with self.assertSQLQueries():
            Car.objects.bulk_create([
                Car(wheel_number=3),
                Car(wheel_number=3, manufacturer="Nissan")])

        self.assertFalse(
            Car.objects.filter(manufacturer="Nissan").exists())
