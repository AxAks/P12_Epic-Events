from django.contrib import admin
from events.models import Event, EventAssignment

admin.site.register(Event)
admin.site.register(EventAssignment)
