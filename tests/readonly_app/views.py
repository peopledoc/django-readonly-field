from django import http
from django.urls import path

from .models import Car


def test_view(request):
    car = Car.objects.create(manufacturer="Honda", wheel_number=3)
    car.refresh_from_db()

    valid = car.manufacturer == "Renault"
    return http.HttpResponse(
        content_type="text/plain",
        content="OK" if valid else "Fail")


urlpatterns = [path("", test_view)]
