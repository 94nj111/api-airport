from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from airport.models import AirplaneType, Airplane, Airport, Crew, Route, Flight


@receiver([post_save], sender=AirplaneType)
def invalidate_message_cache(sender, instance, **kwargs):
    cache.delete_pattern("*airplane_type_view*")
    
@receiver([post_save], sender=Airplane)
def invalidate_message_cache(sender, instance, **kwargs):
    cache.delete_pattern("*airplane_view*")
    
@receiver([post_save], sender=Airport)
def invalidate_message_cache(sender, instance, **kwargs):
    cache.delete_pattern("*airport_view*")
    
@receiver([post_save], sender=Crew)
def invalidate_message_cache(sender, instance, **kwargs):
    cache.delete_pattern("*crew_view*")
    
@receiver([post_save], sender=Route)
def invalidate_message_cache(sender, instance, **kwargs):
    cache.delete_pattern("*route_view*")
    
@receiver([post_save], sender=Flight)
def invalidate_message_cache(sender, instance, **kwargs):
    cache.delete_pattern("*flight_view*")
