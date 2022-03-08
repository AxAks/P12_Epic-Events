from django.contrib import admin

from api.models import Client, Contract, Event, ClientAssignment, ContractAssignment, EventAssignment

admin.site.register(Client)
admin.site.register(Contract)
admin.site.register(Event)

admin.site.register(ClientAssignment)
admin.site.register(ContractAssignment)
admin.site.register(EventAssignment)

