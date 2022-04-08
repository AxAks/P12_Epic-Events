from django.contrib import admin

from api.models import Client, Contract, Event, ClientAssignment, ContractNegotiationAssignment, \
    ContractSignatureAssignment, EventAssignment

admin.site.register(Client)
admin.site.register(Contract)
admin.site.register(Event)

admin.site.register(ClientAssignment)
admin.site.register(ContractNegotiationAssignment)
admin.site.register(ContractSignatureAssignment)
admin.site.register(EventAssignment)

