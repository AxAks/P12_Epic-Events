from django.contrib import admin
from django.contrib.admin import ModelAdmin

from api.models import Client, Contract, Event, ClientAssignment, ContractNegotiationAssignment, \
    ContractSignatureAssignment, EventAssignment, ContractPaymentAssignment


@admin.register(Client)
class ClientAdmin(ModelAdmin):
    list_display = ('first_name', 'last_name', 'company_name', 'email')


@admin.register(Contract)
class ContractAdmin(ModelAdmin):
    list_display = ('client', 'amount_in_cts', 'due_date')


@admin.register(Event)
class EventAdmin(ModelAdmin):
    list_display = ('name', 'begin_date', 'end_date', 'status')


@admin.register(ClientAssignment)
class ClientAssignmentAdmin(ModelAdmin):
    list_display = ('client', 'employee', 'date_created')


@admin.register(ContractNegotiationAssignment)
class ContractNegotiationAssignmentAdmin(ModelAdmin):
    list_display = ('contract', 'employee', 'date_created')


@admin.register(ContractSignatureAssignment)
class ContractSignatureAssignmentAdmin(ModelAdmin):
    list_display = ('contract', 'employee', 'date_created')


@admin.register(ContractPaymentAssignment)
class ContractPaymentAssignmentAdmin(ModelAdmin):
    list_display = ('contract', 'employee', 'date_created')


@admin.register(EventAssignment)
class EventAssignmentAdmin(ModelAdmin):
    list_display = ('event', 'employee', 'date_created')

