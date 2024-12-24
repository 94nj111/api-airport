from django.test import TestCase
from airport.models import AirplaneType, Airplane, Airport, Route


class ModelTests(TestCase):
    def test_airplane_capacity(self):
        airplane_type = AirplaneType.objects.create(name="Boeing 737")
        airplane = Airplane.objects.create(
            name="Test Plane",
            rows=20,
            seats_in_row=6,
            airplane_type=airplane_type,
        )
        self.assertEqual(airplane.capacity, airplane.rows * airplane.seats_in_row)

    def test_airport_full_info(self):
        airport = Airport.objects.create(name="Heathrow", closest_big_city="London")
        self.assertEqual(airport.full_info, f"{airport.name} ({airport.closest_big_city})")

    def test_route_str(self):
        source = Airport.objects.create(name="Heathrow", closest_big_city="London")
        destination = Airport.objects.create(name="Charles de Gaulle", closest_big_city="Paris")
        route = Route.objects.create(source=source, destination=destination, distance=350)
        self.assertEqual(str(route), f"{route.source} - {route.destination}")
                         