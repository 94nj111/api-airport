from datetime import datetime

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from airport.permissions import IsAdminOrIfAuthenticatedReadOnly

from airport.models import (
    AirplaneType,
    Airplane,
    Airport,
    Crew,
    Route,
    Flight,
    Order,
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
    FlightDetailSerializer,
    OrderSerializer,
    OrderListSerializer,
)


class AirplaneTypeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class AirplaneViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class AirportViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class CrewViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class RouteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")

        queryset = Route.objects.select_related("source", "destination")

        if source:
            queryset = queryset.filter(source__closest_big_city__icontains=source)

        if destination:
            queryset = queryset.filter(
                destination__closest_big_city__icontains=destination
            )

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer

        if self.action == "retrive":
            return RouteDetailSerializer

        return RouteSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "source",
                type=OpenApiTypes.STR,
                description="Filter by source closest big city (e.g. & ?source=London)",
            ),
            OpenApiParameter(
                "destination",
                type=OpenApiTypes.STR,
                description="Filter by destination closest big city (e.g. & ?destination=Paris)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class FlightViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        route_source = self.request.query_params.get("route_source")
        route_destination = self.request.query_params.get("route_destination")
        departure_date = self.request.query_params.get("departure")
        arrival_date = self.request.query_params.get("arrival")

        queryset = Flight.objects.select_related("route", "airplane")

        if route_source:
            queryset = queryset.filter(
                route__source__closest_big_city__icontains=route_source
            )

        if route_destination:
            queryset = queryset.filter(
                route__destination__closest_big_city__icontains=route_destination
            )

        if departure_date:
            departure_date = datetime.strptime(departure_date, "%Y-%m-%d").date()
            queryset = queryset.filter(departure_time__date=departure_date)

        if arrival_date:
            arrival_date = datetime.strptime(arrival_date, "%Y-%m-%d").date()
            queryset = queryset.filter(arrival_time__date=arrival_date)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer

        if self.action == "retrive":
            return FlightDetailSerializer

        return FlightSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "route_source",
                type=OpenApiTypes.STR,
                description="Filter by flight source closest big city (e.g. & ?route_source=London)",
            ),
            OpenApiParameter(
                "route_destination",
                type=OpenApiTypes.STR,
                description="Filter by flight destination closest big city (e.g. & ?route_destination=Paris)",
            ),
            OpenApiParameter(
                "departure_date",
                type=OpenApiTypes.DATE,
                description=(
                    "Filter by departure date of Flight " "(e.g. ?date=2022-10-23)"
                ),
            ),
            OpenApiParameter(
                "arrival_date",
                type=OpenApiTypes.DATE,
                description=(
                    "Filter by arrival date of Flight " "(e.g. ?date=2022-10-23)"
                ),
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.prefetch_related(
            "ticket__flight__route", "ticket__flight__airplane"
        ).filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer

        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
