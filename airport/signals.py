from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from airport.models import AirplaneType, Airplane, Airport, Crew, Route, Flight


CACHE_PATTERNS = {
    AirplaneType: "*airplane_type_view*",
    Airplane: "*airplane_view*",
    Airport: "*airport_view*",
    Crew: "*crew_view*",
    Route: "*route_view*",
    Flight: "*flight_view*",
}


@receiver(post_save)
def invalidate_cache(sender, instance, **kwargs):
    if sender in CACHE_PATTERNS:
        cache_pattern = CACHE_PATTERNS[sender]
        cache.delete_pattern(cache_pattern)
