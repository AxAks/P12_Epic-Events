from datetime import date, timedelta

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models import DatedItem, Employee, Person

from constants import STATUSES


class Client(Person):
    company_name = models.CharField(_('company name'), max_length=50)
    mobile = models.CharField(_('mobile phone number'), max_length=15, blank=True)

    def __str__(self):
        return f'{self.get_full_name()} ({self.company_name})'


class Contract(DatedItem):
    client = models.ForeignKey(to=Client, related_name='contractor',
                               on_delete=models.CASCADE)  # on delete, à voir... ( passer en AnonymousUser peut etre, cf RGPD)
    sales_person = models.ForeignKey(to=Employee, related_name='related_sales_person',
                                     on_delete=models.CASCADE)  # on delete, à voir... (passer en AnonymousUser peut etre, cf RGPD)
    status = models.BooleanField(_('status'))  # remplacer par is_signed en @property
    amount_in_cts = models.IntegerField(_('amount (in cts)')) # mettre un default = 0
    due_date = models.DateTimeField(_('due_date'), null=False, default=timezone.now)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        now = timezone.now()
        self.due_date = now + timedelta(days=90)

    @property
    def related_client_company_name(self):
        return self.client.company_name

    @property
    def related_event_name(self):
        return Event.objects.filter(contract=self).first().name \
            if Event.objects.filter(contract=self).first() else '(No related event yet)'

    @property
    def amount_in_euros(self):
        return self.amount_in_cts / 100

    def __str__(self):
        return f'{self.related_client_company_name}, {self.related_event_name}: {self.amount_in_euros}€'


class Event(DatedItem):
    contract = models.OneToOneField(to=Contract, related_name='event_contract',
                                    on_delete=models.CASCADE)  # on delete, à voir... ( passer en AnonymousUser peut etre, cf RGPD)
    name = models.CharField(_('event_name'), max_length=50)
    status = models.IntegerField(choices=STATUSES) # ils demandent une ForeignKey ici ???, liée au statut du contrat ???
    begin_date = models.DateTimeField(_('begin date'))
    end_date = models.DateTimeField(_('end date'))
    attendees = models.IntegerField(_('attendees'), default=0)
    notes = models.TextField(_('notes'))

    def __str__(self):
        return f'{self.name}: {self.begin_date.date()} to {self.end_date.date()}, attendees: {self.attendees}'


class Assignment(DatedItem):
    employee = models.ForeignKey(to=Employee, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class ClientAssignment(Assignment):  # pourquoi ? // ContractAssignment, difference?
    client = models.ForeignKey(to=Client, related_name='assigned_client',
                               on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.client} is assigned to {self.employee}'


class ContractAssignment(Assignment):  # pourquoi ? // ClientAssignment, difference?
    contract = models.ForeignKey(to=Contract, related_name='assigned_contract',
                                 on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.contract} is assigned to {self.employee}'


class EventAssignment(Assignment):
    event = models.ForeignKey(to=Event, related_name='assigned_event',
                              on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.event}  is assigned to {self.employee}'
