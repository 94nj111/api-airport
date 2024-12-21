from django.db import models
from base.models import UUIDModel
from django.conf import settings
from django.core.exceptions import ValidationError


class AirplaneType(UUIDModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Airplane(UUIDModel):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(
        AirplaneType, on_delete=models.CASCADE, related_name="airplanes"
    )

    def __str__(self):
        return f"{self.airplane_type} {self.name}: (rows: {self.rows}, seats in row: {self.seats_in_row})"


class Airport(UUIDModel):
    name = models.CharField(max_length=255)
    closest_big_city = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}: {self.closest_big_city}"


class Route(UUIDModel):
    source = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="source_routes"
    )
    destination = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="destination_routes"
    )
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.source} - {self.destination}"


class Flight(UUIDModel):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="flights")
    airplane = models.ForeignKey(
        Airplane, on_delete=models.CASCADE, related_name="flights"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        return f"{self.route} | {self.airplane} | {self.departure_time} - {self.arrival_time}"


class Crew(UUIDModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    flights = models.ManyToManyField(Flight, related_name="crews")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Order(UUIDModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )

    def __str__(self):
        return f"{self.user.email}: {self.created_at}"


class Ticket(UUIDModel):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="tickets")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")

    @staticmethod
    def validate_ticket(ticket_row, ticket_seat, airplane_id):
        for ticket_attr_value, ticket_attr_name, airplane_attr_name in [
            (ticket_row, "row", "rows"),
            (ticket_seat, "seat", "seats_in_row"),
        ]:
            airplane = Airplane.objects.get(pk=airplane_id)
            count_attrs = getattr(airplane, airplane_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise ValidationError(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                        f"number must be in available range: "
                        f"(1, {airplane_attr_name}): "
                        f"(1, {count_attrs})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(self.row, self.seat, self.movie_session.cinema_hall.id)

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.full_clean()
        super(Ticket, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f"{str(self.flight)} (row: {self.row}, seat: {self.seat})"

    class Meta:
        unique_together = ("flight", "row", "seat")
        ordering = (
            "row",
            "seat",
        )
