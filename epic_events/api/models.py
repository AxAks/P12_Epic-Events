from django.db import models
from django.db.models import FloatField
from django.utils.translation import gettext_lazy as _

from core.models import DatedItem, Employee, Person

from constants import STATUSES


class Client(Person):
    company_name = models.CharField(_('company name'), max_length=50)
    mobile = models.CharField(_('mobile phone number'), max_length=15)


class Contract(DatedItem):
    client = models.ForeignKey(to=Client, related_name='contractor',
                               on_delete=models.CASCADE)  # on delete, à voir... ( passer en AnonymousUser peut etre, cf RGPD)
    sales_person = models.ForeignKey(to=Employee, related_name='related_sales_person',
                                     on_delete=models.CASCADE)  # on delete, à voir... ( passer en AnonymousUser peut etre, cf RGPD)
    status = models.BooleanField(_('status')) # mettre default=False, voir à quoi peut servir ce champs
    amount_in_cts = models.IntegerField(_('amount')) # mettre un default = 0
    due_date = models.DateTimeField(_('due_date'))  # mettre une date par defaut dans le futur à partir de la date de creation


class Event(DatedItem):
    contract = models.ForeignKey(to=Contract, related_name='event_contract',
                                 on_delete=models.CASCADE)  # on delete, à voir... ( passer en AnonymousUser peut etre, cf RGPD)
    status = models.CharField(max_length=10, choices=STATUSES) # ils demandent une ForeignKey ici ???, liée au statut du contrat ???
    begin_date = models.DateTimeField(_('begin date'))
    end_date = models.DateTimeField(_('end date'))
    attendees = models.IntegerField(_('attendees')) # mettre un default=0
    notes = models.TextField(_('notes')) # mettre un default=''


class Assignment(DatedItem):
    employee = models.ForeignKey(to=Employee, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class ClientAssignment(Assignment):  # pourquoi ? // ContractAssignment, difference?
    client = models.ForeignKey(to=Client, related_name='assigned_client',
                               on_delete=models.CASCADE)


class ContractAssignment(Assignment):  # pourquoi ? // ClientAssignment, difference?
    contract = models.ForeignKey(to=Contract, related_name='assigned_contract',
                                 on_delete=models.CASCADE)


class EventAssignment(Assignment):
    event = models.ForeignKey(to=Event, related_name='assigned_event',
                              on_delete=models.CASCADE)
