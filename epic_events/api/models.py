from datetime import date, timedelta

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models import DatedItem, Employee, Person

from constants import STATUSES


class Client(Person):
    company_name = models.CharField(_('company name'), max_length=50)
    mobile = models.CharField(_('mobile phone number'), max_length=15, blank=True)

    @property
    def is_prospect(self) -> bool:
        return Contract.objects.filter(client=self).exists()

    def __str__(self):
        return f'{self.get_full_name()} ({self.company_name})'


class Contract(DatedItem):
    client = models.ForeignKey(to=Client, related_name='contractor',
                               on_delete=models.CASCADE)  # on delete, à voir... ( passer en AnonymousUser peut etre, cf RGPD)
    sales_person = models.ForeignKey(to=Employee, related_name='related_sales_person',
                                     on_delete=models.CASCADE)  # on delete, à voir... (passer en AnonymousUser peut etre, cf RGPD)
    amount_in_cts = models.IntegerField(_('amount (in cts)')) # mettre un default = 0
    due_date = models.DateTimeField(_('due_date'), null=False, default=timezone.now)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        now = timezone.now()
        self.due_date = now + timedelta(days=90)

    @property
    def is_signed(self) -> bool:
        return ContractSignatureAssignment.objects.filter(contract=self).exists()

    @property
    def related_client_company_name(self):
        return self.client.company_name

    @property
    def related_event_name(self):
        return Event.objects.filter(contract=self).first().name \
            if Event.objects.filter(contract=self).first() else '(No related event yet)'

    @property
    def amount_in_euros(self) -> float:
        return round(self.amount_in_cts / 100, 2)

    def __str__(self):
        return f'{self.related_client_company_name}, {self.related_event_name}: {self.amount_in_euros}€'


class Event(DatedItem):
    contract = models.OneToOneField(to=Contract, related_name='event_contract',
                                    on_delete=models.CASCADE)  # on delete, à voir... ( passer en AnonymousUser peut etre, cf RGPD)
    name = models.CharField(_('event_name'), max_length=50)
    status = models.IntegerField(choices=STATUSES)
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


class ClientAssignment(Assignment):  # pour le suivi du passage de is_prospect True à False
    client = models.ForeignKey(to=Client, related_name='assigned_client',
                               on_delete=models.CASCADE)

    def to_sales(self):
        return self.employee.is_sales

    def __str__(self):
        return f'{self.client} prospecting led by {self.employee}'


class ContractAssignment(Assignment):

    class Meta:
        abstract = True


class ContractNegotiationAssignment(ContractAssignment):  # pour le suivi de la nego du contract de is_signed = False à True
    contract = models.ForeignKey(to=Contract, related_name='assigned_contract',
                                 on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.contract} negotiation led by {self.employee}'


class ContractSignatureAssignment(ContractAssignment):  # pour connaitre le statut de signature du contract et la date + l'employee qui a signé
    contract = models.ForeignKey(to=Contract, related_name='signature_contract_status',
                                 on_delete=models.CASCADE)

    def to_sales(self):
        return self.employee.is_sales

    def assignable(self):
        return self.contract.is_signed

    def __str__(self):
        return f'{self.contract} signature followed by {self.employee}'


class ContractPaymentAssignment(ContractAssignment):  # pour savoir si/quand le paiement du contract à été effectué + l'employee qui a enregistré le paiement
    contract = models.ForeignKey(to=Contract, related_name='payment_contract_status',
                                 on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.contract} signature followed by {self.employee}'


class EventAssignment(Assignment):
    event = models.ForeignKey(to=Event, related_name='assigned_event',
                              on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.event}  is assigned to {self.employee}'
