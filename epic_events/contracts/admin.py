from django.contrib import admin
from contracts.models import Contract, ClientAssignment, ContractAssignment

admin.site.register(Contract)
admin.site.register(ClientAssignment)
admin.site.register(ContractAssignment)
