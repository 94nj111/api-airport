from django.test import TestCase
from airport.models import (
    AirplaneType,
    Airplane,
    Airport,
    Route,
    Flight,
    Crew,
)
from airport.serializers import (
    AirplaneTypeSerializer,
    AirplaneSerializer,
    AirportSerializer,
    CrewSerializer,
    RouteSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
    FlightSerializer,
    FlightListSerializer,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class AirplaneTypeSerializerTests(TestCase):
    def test_airplane_type_serializer(self):
        airplane_type = AirplaneType.objects.create(name="Boeing 737")
        serializer = AirplaneTypeSerializer(instance=airplane_type)
        self.assertEqual(serializer.data, {"id": airplane_type.id, "name": "Boeing 737"})


class AirplaneSerializerTests(TestCase):
    def test_airplane_serializer(self):
        airplane_type = AirplaneType.objects.create(name="Boeing 737")
        airplane = Airplane.objects.create(
            name="Test Plane", rows=20, seats_in_row=6, airplane_type=airplane_type
        )
        serializer = AirplaneSerializer(instance=airplane)
        self.assertEqual(
            serializer.data,
            {
                "id": airplane.id,
                "name": "Test Plane",
                "rows": 20,
                "seats_in_row": 6,
                "capacity": 120,
                "airplane_type": airplane_type.id,
            },
        )


class AirportSerializerTests(TestCase):
    def test_airport_serializer(self):
        airport = Airport.objects.create(name="Heathrow", closest_big_city="London")
        serializer = AirportSerializer(instance=airport)
        self.assertEqual(
            serializer.data,
            {"id": airport.id, "name": "Heathrow", "closest_big_city": "London"},
        )


class CrewSerializerTests(TestCase):
    def test_crew_serializer(self):
        crew = Crew.objects.create(first_name="John", last_name="Doe")
        serializer = CrewSerializer(instance=crew)
        self.assertEqual(
            serializer.data, {"id": crew.id, "first_name": "John", "last_name": "Doe"}
        )


class RouteSerializerTests(TestCase):
    def setUp(self):
        self.source = Airport.objects.create(name="Heathrow", closest_big_city="London")
        self.destination = Airport.objects.create(
            name="Charles de Gaulle", closest_big_city="Paris"
        )
        self.route = Route.objects.create(
            source=self.source, destination=self.destination, distance=350
        )

    def test_route_serializer(self):
        serializer = RouteSerializer(instance=self.route)
        self.assertEqual(
            serializer.data,
            {
                "id": self.route.id,
                "source": self.source.id,
                "destination": self.destination.id,
                "distance": 350,
            },
        )

    def test_route_list_serializer(self):
        serializer = RouteListSerializer(instance=self.route)
        self.assertEqual(
            serializer.data,
            {
                "id": self.route.id,
                "source": f"{self.source.name} ({self.source.closest_big_city})",
                "destination": f"{self.destination.name} ({self.destination.closest_big_city})",
                "distance": 350,
            },
        )

    def test_route_detail_serializer(self):
        serializer = RouteDetailSerializer(instance=self.route)
        self.assertEqual(
            serializer.data,
            {
                "id": self.route.id,
                "source": {
                    "id": self.source.id,
                    "name": "Heathrow",
                    "closest_big_city": "London",
                },
                "destination": {
                    "id": self.destination.id,
                    "name": "Charles de Gaulle",
                    "closest_big_city": "Paris",
                },
                "distance": 350,
            },
        )


class FlightSerializerTests(TestCase):
    def setUp(self):
        self.source = Airport.objects.create(name="Heathrow", closest_big_city="London")
        self.destination = Airport.objects.create(
            name="Charles de Gaulle", closest_big_city="Paris"
        )
        self.route = Route.objects.create(
            source=self.source, destination=self.destination, distance=350
        )
        self.airplane_type = AirplaneType.objects.create(name="Boeing 737")
        self.airplane = Airplane.objects.create(
            name="Test Plane", rows=20, seats_in_row=6, airplane_type=self.airplane_type
        )
        self.flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time="2024-01-01T10:00:00Z",
            arrival_time="2024-01-01T12:00:00Z",
        )

    def test_flight_serializer(self):
        serializer = FlightSerializer(instance=self.flight)
        self.assertEqual(
            serializer.data,
            {
                "id": self.flight.id,
                "route": self.route.id,
                "airplane": self.airplane.id,
                "departure_time": "2024-01-01T10:00:00Z",
                "arrival_time": "2024-01-01T12:00:00Z",
            },
        )

    def test_flight_list_serializer(self):
        serializer = FlightListSerializer(instance=self.flight)
        self.assertEqual(
            serializer.data,
            {
                "id": self.flight.id,
                "route_source": f"{self.source.name} ({self.source.closest_big_city})",
                "route_destination": f"{self.destination.name} ({self.destination.closest_big_city})",
                "departure_time": self.flight.departure_time,
                "arrival_time": self.flight.arrival_time,
                "airplane_name": "Test Plane",
                "airplane_capacity": 120,
                "tickets_available": 120,
            },
        )
