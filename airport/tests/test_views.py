from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.urls import reverse

from airport.models import (
    AirplaneType,
    Airplane,
    Airport,
    Route,
    Flight,
)

User = get_user_model()


class ViewSetTests(APITestCase):
    AIRPLANE_TYPE_LIST = reverse("airport:airplane-types-list")
    AIRPLANE_LIST = reverse("airport:airplanes-list")
    AIRPORT_LIST = reverse("airport:airports-list")
    ROUTE_LIST = reverse("airport:routes-list")
    FLIGHT_LIST = reverse("airport:flights-list")
    ORDER_LIST = reverse("airport:orders-list")

    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com", password="password123"
        )
        self.admin_user = User.objects.create_superuser(
            email="admin@example.com", password="admin123"
        )

        self.airplane_type = AirplaneType.objects.create(name="Boeing 737")
        self.airport1 = Airport.objects.create(
            name="Heathrow", closest_big_city="London"
        )
        self.airport2 = Airport.objects.create(
            name="Charles de Gaulle", closest_big_city="Paris"
        )
        self.route = Route.objects.create(
            source=self.airport1, destination=self.airport2, distance=350
        )
        self.airplane = Airplane.objects.create(
            name="Test Plane", rows=20, seats_in_row=6, airplane_type=self.airplane_type
        )
        self.flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time="2024-01-01T10:00:00Z",
            arrival_time="2024-01-01T12:00:00Z",
        )

    def authenticate(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_airplane_type_list(self):
        self.authenticate(self.user)
        response = self.client.get(self.AIRPLANE_TYPE_LIST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_airplane_type_create_admin_only(self):
        self.authenticate(self.user)
        response = self.client.post(self.AIRPLANE_TYPE_LIST, {"name": "Airbus A320"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.authenticate(self.admin_user)
        response = self.client.post(self.AIRPLANE_TYPE_LIST, {"name": "Airbus A320"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_airplane_list(self):
        self.authenticate(self.user)
        response = self.client.get(self.AIRPLANE_LIST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_airplane_create_admin_only(self):
        data = {
            "name": "New Plane",
            "rows": 10,
            "seats_in_row": 4,
            "airplane_type": self.airplane_type.id,
        }
        self.authenticate(self.user)
        response = self.client.post(self.AIRPLANE_LIST, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.authenticate(self.admin_user)
        response = self.client.post(self.AIRPLANE_LIST, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_airport_list(self):
        self.authenticate(self.user)
        response = self.client.get(self.AIRPORT_LIST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_airport_create_admin_only(self):
        data = {"name": "LAX", "closest_big_city": "Los Angeles"}
        self.authenticate(self.user)
        response = self.client.post(self.AIRPORT_LIST, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.authenticate(self.admin_user)
        response = self.client.post(self.AIRPORT_LIST, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_route_list(self):
        self.authenticate(self.user)
        response = self.client.get(self.ROUTE_LIST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_route_create_admin_only(self):
        data = {
            "source": self.airport1.id,
            "destination": self.airport2.id,
            "distance": 500,
        }
        self.authenticate(self.user)
        response = self.client.post(self.ROUTE_LIST, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.authenticate(self.admin_user)
        response = self.client.post(self.ROUTE_LIST, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_flight_list(self):
        self.authenticate(self.user)
        response = self.client.get(self.FLIGHT_LIST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_flight_create_admin_only(self):
        data = {
            "route": self.route.id,
            "airplane": self.airplane.id,
            "departure_time": "2024-01-02T10:00:00Z",
            "arrival_time": "2024-01-02T12:00:00Z",
        }
        self.authenticate(self.user)
        response = self.client.post(self.FLIGHT_LIST, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.authenticate(self.admin_user)
        response = self.client.post(self.FLIGHT_LIST, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_order_list_user_only(self):
        self.authenticate(self.user)
        response = self.client.get(self.ORDER_LIST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_create_unauthenticated(self):
        response = self.client.post(self.ORDER_LIST, {"tickets": []})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
