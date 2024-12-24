from django.contrib import admin

from airport.models import (
    AirplaneType,
    Airplane,
    Airport,
    Crew,
    Route,
    Flight,
    Ticket,
    Order,
)

admin.site.register(AirplaneType)
admin.site.register(Airplane)
admin.site.register(Airport)
admin.site.register(Crew)
admin.site.register(Route)
admin.site.register(Flight)
admin.site.register(Ticket)
admin.site.register(Order)
