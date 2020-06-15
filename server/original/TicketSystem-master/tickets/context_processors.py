from .models import *


def max_event_id(request):
    if Event.objects.values_list('pk', flat=True):
        return {
            'max_event_id': str(max(Event.objects.values_list('pk', flat=True)))
        }
