from contextlib import contextmanager
import json

import requests
import six

from django.test import TestCase
from django.test import LiveServerTestCase
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.core import serializers

# Create your tests here.
from tests.readonly_app.models import Car
from tests.readonly_app.models import Bus
from tests.readonly_app.models import Book


class ReadonlyFieldTest(TestCase):

    # Note : the default for fields is in the file 0002_sql_default.py
    # Default values are :
    # Car: manufacturer = "Renault"
    # Bus: wheel_number = 22
    # Book: iban = "1234-abcd", ref = 123456789

    @classmethod
    def setUpTestData(cls):
        cls.peugeot_car = Car.objects.create(wheel_number=5)
        connection.cursor().execute(
            "UPDATE readonly_app_car "
            "SET manufacturer='Peugeot' WHERE id=%s",
            [cls.peugeot_car.pk])

    def setUp(self):
        self.peugeot_car.refresh_from_db()

    @contextmanager
    def assertSQLQueries(self, model=None, check_other_fields=True):
        """
        Asserts that the SQL from the queries don't mention
        the readonly field. SELECTS are authorized, though.
        model allow you to specify the model for which readonly
        fields will be checked
        """
        model = model or Car
        readonly_fields = model.ReadonlyMeta.readonly
        with CaptureQueriesContext(connection=connection) as capture:
            yield capture

        unchecked_queries = frozenset("SELECT SAVEPOINT RELEASE".split())

        for query in self._filter_queries(capture, exclude=unchecked_queries):

            for field in readonly_fields:
                self.assertNotIn(field, query['sql'])

            if check_other_fields:
                fields = {field.name
                          for field in model._meta.fields
                          if not field.primary_key}
                read_write_fields = fields - frozenset(readonly_fields)
                for field in read_write_fields:
                    self.assertIn(field, query['sql'])

    def _filter_queries(self, capture, include=None, exclude=None):
        for query in capture.captured_queries:
            command = query['sql'].split()[0]
            if include:
                if command in include:
                    yield query
            if exclude:
                if command not in exclude:
                    yield query

    def assertNumCommands(self, capture, command, count):
        queries = list(self._filter_queries(capture, include={command}))
        num_queries = len(queries)
        self.assertEqual(
            num_queries,
            count,
            "{num_queries} {command} query(ies) found. "
            "Expected {count}. \n Queries: {queries}".format(
                num_queries=num_queries, command=command,
                count=count, queries="\n".join(
                    q['sql'] for q in queries)))

    def test_create(self):
        # Create, don't specify the readonly field
        with self.assertSQLQueries():
            car = Car.objects.create(wheel_number=4)

        car.refresh_from_db()

        self.assertEqual(car.wheel_number, 4)
        self.assertEqual(car.manufacturer, "Renault")

        # Create, do specify the readonly field
        with self.assertSQLQueries():
            car = Car.objects.create(manufacturer="Honda", wheel_number=3)

        car.refresh_from_db()
        self.assertEqual(car.manufacturer, "Renault")
        self.assertEqual(car.wheel_number, 3)

    def test_save(self):
        # Save a new instance, don't specify the readonly field
        with self.assertSQLQueries():
            car = Car(wheel_number=3)
            car.save()

        car.refresh_from_db()

        self.assertEqual(car.manufacturer, "Renault")
        self.assertEqual(car.wheel_number, 3)

        # Save a new instance, do specify the readonly field
        with self.assertSQLQueries():
            car = Car(wheel_number=3, manufacturer="Opel")
            car.save()

        car.refresh_from_db()
        self.assertEqual(car.manufacturer, "Renault")
        self.assertEqual(car.wheel_number, 3)

    def test_save_update(self):
        # Save an existing instance
        car = self.peugeot_car

        with self.assertSQLQueries():
            car.save()

        car.refresh_from_db()
        self.assertEqual(car.manufacturer, "Peugeot")
        self.assertEqual(car.wheel_number, 5)

        # Save an existing instance, don't specify the readonly field
        with self.assertSQLQueries():
            car.wheel_number = 7
            car.save()

        car.refresh_from_db()
        self.assertEqual(car.manufacturer, "Peugeot")
        self.assertEqual(car.wheel_number, 7)

        # Save an existing instance, do specify the readonly field
        with self.assertSQLQueries():
            car.manufacturer = "Citroen"
            car.save()

        car.refresh_from_db()
        self.assertEqual(car.manufacturer, "Peugeot")
        self.assertEqual(car.wheel_number, 7)

    def test_update(self):
        # Update, don't specify the readonly field
        car = self.peugeot_car
        with self.assertSQLQueries():
            Car.objects.filter(pk=car.pk).update(wheel_number=12)

        car.refresh_from_db()
        self.assertEqual(car.manufacturer, "Peugeot")
        self.assertEqual(car.wheel_number, 12)

        # Update, do specify the readonly field
        with self.assertSQLQueries():
            Car.objects.filter(pk=car.pk).update(manufacturer="Ferrari")

        car.refresh_from_db()
        self.assertEqual(car.manufacturer, "Peugeot")
        self.assertEqual(car.wheel_number, 12)

        # Update both
        with self.assertSQLQueries():
            Car.objects.filter(pk=car.pk).update(
                manufacturer="Ferrari", wheel_number=52)

        car.refresh_from_db()
        self.assertEqual(car.manufacturer, "Peugeot")
        self.assertEqual(car.wheel_number, 52)

    def test_get_or_create(self):
        # get_or_create, don't specify the readonly field
        with self.assertSQLQueries():
            car, __ = Car.objects.get_or_create(wheel_number=3)

        car.refresh_from_db()
        self.assertEqual(car.manufacturer, "Renault")

        # get_or_create, do specify the readonly field
        with self.assertSQLQueries():
            car, __ = Car.objects.get_or_create(
                wheel_number=3,
                defaults={"manufacturer": "Volkswagen"})

        car.refresh_from_db()
        self.assertEqual(car.manufacturer, "Renault")
        self.assertEqual(car.wheel_number, 3)

        # (we're not testing the get part because it doesn't involve a write)

    def test_bulk_create(self):

        # bulk_create, do and don't specify the readonly field
        latest_car_pk = Car.objects.latest("pk").pk
        queryset = Car.objects.filter(pk__gt=latest_car_pk)

        with self.assertSQLQueries():
            Car.objects.bulk_create([
                Car(wheel_number=3),
                Car(wheel_number=3, manufacturer="Nissan")])

        # 2 cars were saved
        self.assertEqual(queryset.count(), 2)

        # No car exists with "Nissan"
        self.assertFalse(
            queryset.filter(manufacturer="Nissan").exists())

        # All cars have 3 wheels (what ?!)
        self.assertTrue(all(
            car.wheel_number == 3 for car in queryset))

    def test_serialize(self):
        serialized = json.loads(serializers.serialize(
            "json",
            Car.objects.filter(id=self.peugeot_car.id)))

        self.assertEqual(len(serialized), 1)

        dict_car, = serialized

        self.assertIn("wheel_number", dict_car["fields"])
        self.assertIn("manufacturer", dict_car["fields"])

    def test_deserialize(self):
        pk = Car.objects.latest("id").id + 1
        json_car = json.dumps([{"model": "readonly_app.car",
                                "pk": pk,
                                "fields": {"wheel_number": 12,
                                           "manufacturer": "Volvo"}}])

        # Check that the save works
        with self.assertSQLQueries(Car) as capture:
            deserialized = serializers.deserialize("json", json_car)

            car, = deserialized
            car.save()

        # Because a pk is specified, Django will try to do an UPDATE and then
        # an INSERT when the UPDATE returns with 0 rows affected
        self.assertNumCommands(capture, command="UPDATE", count=1)
        self.assertNumCommands(capture, command="INSERT", count=1)

        car = Car.objects.get(pk=pk)
        self.assertEqual(car.wheel_number, 12)
        self.assertEqual(car.manufacturer, "Renault")

        json_car = json_car.replace("12", "14")
        # Check that the UPDATE works
        with self.assertSQLQueries(Car) as capture:
            deserialized = serializers.deserialize("json", json_car)

            car, = deserialized
            car.save()

        self.assertNumCommands(capture, command="UPDATE", count=1)
        self.assertNumCommands(capture, command="INSERT", count=0)

        car = Car.objects.get(pk=pk)
        self.assertEqual(car.wheel_number, 14)
        self.assertEqual(car.manufacturer, "Renault")

    def test_several_models(self):

        # We make sure that using several models together don't result
        # in an error. In particular, car and bus have properties of the
        # same name but not the same "readonly" state.

        # First without specifying the readonly field
        with self.assertSQLQueries(Car):
            car = Car.objects.create(wheel_number=4)
        with self.assertSQLQueries(Bus):
            bus = Bus.objects.create(manufacturer="Audi")
        with self.assertSQLQueries(Book):
            book = Book.objects.create(name="Farenheit 411")

        car.refresh_from_db()
        self.assertEqual(car.manufacturer, "Renault")
        self.assertEqual(car.wheel_number, 4)

        bus.refresh_from_db()
        self.assertEqual(bus.wheel_number, 22)
        self.assertEqual(bus.manufacturer, "Audi")

        book.refresh_from_db()
        self.assertEqual(book.name, "Farenheit 411")
        self.assertEqual(book.ref, 123456789)
        self.assertEqual(book.iban, "1234-abcd")

        # Then, specifying the readonly field
        with self.assertSQLQueries(Car):
            car = Car.objects.create(
                wheel_number=4, manufacturer="Lamborghini")
        with self.assertSQLQueries(Bus):
            bus = Bus.objects.create(
                manufacturer="Audi", wheel_number=17)
        with self.assertSQLQueries(Book):
            book = Book.objects.create(
                name="Harry Potter", ref=4321, iban="zyxw-9876")

        car.refresh_from_db()
        self.assertEqual(car.manufacturer, "Renault")
        self.assertEqual(car.wheel_number, 4)

        bus.refresh_from_db()
        self.assertEqual(bus.wheel_number, 22)
        self.assertEqual(bus.manufacturer, "Audi")

        book.refresh_from_db()
        self.assertEqual(book.name, "Harry Potter")
        self.assertEqual(book.ref, 123456789)
        self.assertEqual(book.iban, "1234-abcd")


class ReadonlyFieldRunserverTest(LiveServerTestCase):
    def test_run_server(self):
        self.assertEqual(
            requests.get(self.live_server_url).content,
            six.b("OK"))
