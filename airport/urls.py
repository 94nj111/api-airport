from rest_framework.routers import DefaultRouter
from django.urls import path, include

from airport.views import (
    AirplaneTypeViewSet,
    AirplaneViewSet,
    AirportViewSet,
    CrewViewSet,
    RouteViewSet,
    FlightViewSet,
    OrderViewSet,
)

router = DefaultRouter()
router.register("airplane-types", AirplaneTypeViewSet, basename="airplane-types")
router.register("airplanes", AirplaneViewSet, basename="airplanes")
router.register("airports", AirportViewSet, basename="airports")
router.register("crews", CrewViewSet, basename="crews")
router.register("routes", RouteViewSet, basename="routes")
router.register("flights", FlightViewSet, basename="flights")
router.register("orders", OrderViewSet, basename="orders")

urlpatterns = [path("", include(router.urls))]

app_name = "airport"
