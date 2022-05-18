from django.contrib import admin
from django.contrib.admin import ModelAdmin

from api.models import Client, Contract, Event, ClientAssignment, ContractNegotiationAssignment, \
    ContractSignatureAssignment, EventAssignment, ContractPaymentAssignment


@admin.register(Client)
class ClientAdmin(ModelAdmin):
    list_display = ['first_name', 'last_name', 'company_name', 'email']
    list_filter = ['last_name', 'company_name', 'email']
    search_fields = ['first_name', 'last_name', 'company_name', 'email']
    search_help_text = "Search by: name, email or company name"


@admin.register(Contract)
class ContractAdmin(ModelAdmin):
    list_display = ['client', 'amount_in_cts', 'date_created', 'due_date']
    list_filter = ['client__last_name', 'client__company_name', 'client__email',
                   'amount_in_cts', 'date_created',
                   'due_date']
    search_fields = ['client__first_name', 'client__last_name', 'client__company_name', 'client__email',
                     'date_created', 'amount_in_cts', 'due_date']
    search_help_text = "Search by: client name or email or company name; contract date, amount or due date"


@admin.register(Event)
class EventAdmin(ModelAdmin):
    list_display = ['name', 'begin_date', 'end_date', 'contract', 'status']
    list_filter = ['name',
                   'contract__client__last_name',
                   'contract__client__company_name', 'contract__client__email',
                   'begin_date', 'end_date', 'status']
    search_fields = ['name',
                     'contract__client__first_name', 'contract__client__last_name',
                     'contract__client__company_name', 'contract__client__email',
                     'begin_date', 'end_date', 'status']
    search_help_text = "Search by: client name, email or company name, event name, begin or end date or status"


@admin.register(ClientAssignment)
class ClientAssignmentAdmin(ModelAdmin):
    list_display = ['client', 'employee', 'date_created']
    list_filter = ['client__last_name', 'client__company_name', 'client__email',
                   'employee__first_name', 'employee__last_name', 'employee__email',
                   'date_created']
    search_fields = ['client__last_name', 'client__company_name', 'client__email',
                     'employee__first_name', 'employee__last_name', 'employee__email',
                     'date_created']
    search_help_text = "Search by: client name, email or company name, assignee name, email, or assignment date"


@admin.register(ContractNegotiationAssignment)
class ContractNegotiationAssignmentAdmin(ModelAdmin):
    list_display = ['contract', 'employee', 'date_created']
    list_filter = ['contract__client__last_name', 'contract__client__company_name', 'contract__client__email',
                   'employee__first_name', 'employee__last_name', 'employee__email',
                   'date_created']
    search_fields = ['contract__client__last_name', 'contract__client__company_name', 'contract__client__email',
                     'employee__first_name', 'employee__last_name', 'employee__email',
                     'date_created']
    search_help_text = "Search by: client name, email or company name, assignee name, email, or assignment date"


@admin.register(ContractSignatureAssignment)
class ContractSignatureAssignmentAdmin(ModelAdmin):
    list_display = ['contract', 'employee', 'date_created']
    list_filter = ['contract__client__last_name', 'contract__client__company_name', 'contract__client__email',
                   'employee__first_name', 'employee__last_name', 'employee__email',
                   'date_created']
    search_fields = ['contract__client__last_name', 'contract__client__company_name', 'contract__client__email',
                     'employee__first_name', 'employee__last_name', 'employee__email',
                     'date_created']
    search_help_text = "Search by: client name, email or company name, assignee name, email, or signature date"


@admin.register(ContractPaymentAssignment)
class ContractPaymentAssignmentAdmin(ModelAdmin):
    list_display = ['contract', 'employee', 'date_created']
    list_filter = ['contract__client__last_name', 'contract__client__company_name', 'contract__client__email',
                   'employee__first_name', 'employee__last_name', 'employee__email',
                   'date_created']
    search_fields = ['contract__client__last_name', 'contract__client__company_name', 'contract__client__email',
                     'employee__first_name', 'employee__last_name', 'employee__email',
                     'date_created']
    search_help_text = "Search by: client name, email or company name, assignee name, email, or payment date"


@admin.register(EventAssignment)
class EventAssignmentAdmin(ModelAdmin):
    list_display = ['event',
                    'employee',
                    'date_created']
    list_filter = ['event__contract__client__last_name', 'event__contract__client__company_name',
                   'event__contract__client__email',
                   'employee__first_name', 'employee__last_name', 'employee__email',
                   'date_created']
    search_fields = ['event__contract__client__last_name', 'event__contract__client__company_name',
                     'event__contract__client__email',
                     'employee__first_name', 'employee__last_name', 'employee__email',
                     'date_created']
    search_help_text = "Search by: client name, email or company name, assignee name, email, or assignment date"
