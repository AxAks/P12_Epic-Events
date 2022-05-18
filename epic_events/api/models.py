from datetime import timedelta

from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models import DatedItem, Employee, Person

from constants import STATUSES


class Client(Person):
    """
    Model for Client
    """
    company_name = models.CharField(_('company name'), max_length=50)
    mobile = models.CharField(_('mobile phone number'), max_length=15, blank=True)

    @property
    def is_assigned(self) -> bool:
        """
        Checks whether a given client is assigned to a sales employee during conversion phase.
        and advises about the employee who was in charge once the client is converted
        """
        return ClientAssignment.objects.filter(client=self).exists()

    @property
    def is_prospect(self) -> bool:
        """
        Checks whether a given client is still a prospect or already a client.
        A client is not a prospect anymore if they have at least one contract registered
        """
        return not Contract.objects.filter(client=self).exists()

    def __str__(self):
        return f'{self.get_full_name()} ({self.company_name})'


class Contract(DatedItem):
    """
    Model for Contract
    """
    client = models.ForeignKey(to=Client, related_name='contractor',
                               on_delete=models.CASCADE)
    amount_in_cts = models.IntegerField(_('amount (in cts)'))
    due_date = models.DateTimeField(_('due_date'), null=False, default=timezone.now)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        now = timezone.now()
        self.due_date = now + timedelta(days=90)

    @property
    def registered_negotiator(self) -> bool:
        """
        Checks whether a given contract is assigned to a sales employee for the negotiation phase
        Until the contract is signed
        """
        return ContractNegotiationAssignment.objects.filter(contract=self).exists()

    @property
    def is_signed(self) -> bool:
        """
        Checks whether a given contract is signed
        """
        return ContractSignatureAssignment.objects.filter(contract=self).exists()

    @property
    def is_paid(self) -> bool:
        """
        Checks whether a given contract has already been paid
        """
        return ContractPaymentAssignment.objects.filter(contract=self).exists()

    @property
    def related_client_company_name(self):
        """
        Returns the company name of the signatory client
        """
        return self.client.company_name

    @property
    def related_event_name(self):
        """
        Returns the name of the related event
        """
        return Event.objects.filter(contract=self).first().name \
            if Event.objects.filter(contract=self).first() else '(No related event yet)'

    @property
    def amount_in_euros(self) -> float:
        """
        Returns the contract value in Euros
        """
        return round(self.amount_in_cts / 100, 2)

    def clean(self):
        """
        validator : checks whether the contract client is assigned to a sales employee
        before the contract can be created
        """
        if not self.client.is_assigned:
            raise ValidationError(
                {NON_FIELD_ERRORS: f'The selected client {self.client}'
                                   f' must be assigned to a sales employee first'})

    def __str__(self):
        return f'{self.related_client_company_name}, {self.related_event_name}: {self.amount_in_euros}€'


class Event(DatedItem):
    """
    Model for Events
    """
    contract = models.OneToOneField(to=Contract, related_name='event_contract',
                                    on_delete=models.CASCADE)
    name = models.CharField(_('event name'), max_length=50)
    status = models.IntegerField(choices=STATUSES)
    begin_date = models.DateTimeField(_('begin date'))
    end_date = models.DateTimeField(_('end date'))
    attendees = models.IntegerField(_('attendees'), default=0)
    notes = models.TextField(_('notes'), blank=True)

    def clean(self):
        """
        validator : checks whether the contract is signed
        before the related event  can be created
        """
        if not self.contract.is_signed:
            raise ValidationError(
                {NON_FIELD_ERRORS: f'The related contract: {self.contract}'
                                   f' must be signed before the event can be created'})

    def __str__(self):
        return f'{self.name} ({self.contract.client.company_name}):'\
               f' {self.begin_date.replace(tzinfo=None)} to {self.end_date.replace(tzinfo=None)},'\
               f' attendees: {self.attendees}'


class Assignment(DatedItem):
    """
    Abstract Parent Class for all types of assignment
    """
    employee = models.ForeignKey(to=Employee, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class ClientAssignment(Assignment):
    """
    Model that links a given client to a sales employee.
    The employee will be in charge during prospection phase
    to convert the prospect
    """
    client = models.OneToOneField(to=Client, related_name='assigned_client',
                                  on_delete=models.CASCADE)

    def unique_error_message(self, model_class, unique_check):
        """
        Overridden error message to unique constraint:
        a client can not be followed by two different employees
        """
        if len(unique_check) == 1:
            return ValidationError(
                message=_(f"{self.client} is already followed"
                          f" by {self.find_assigned_employee_for_client(self.client)}"),
                code="unique",
            )
        else:
            return ValidationError(
                message=_(f"{self.client} is already followed"
                          f" by {self.find_assigned_employee_for_client(self.client)}"),
                code="unique_together",
            )

    def clean(self):
        """
        validator: can only be assigned to an employee that is from the sales department
        """
        if not self.employee.is_sales:
            raise ValidationError(
                {NON_FIELD_ERRORS: f'The selected employee {self.employee}'
                                   f' must be a member of the Sales Department'})

    @classmethod
    def find_assigned_employee_for_client(cls, client):
        """
        Returns the sales employee who is the contact for a given client
        """
        return cls.objects.filter(client=client).first().employee

    def __str__(self):
        return f'{self.client} prospecting led by {self.employee}'


class ContractAssignment(Assignment):
    """
    Abstract Parent Class for all types of contract assignment
    """
    class Meta:
        abstract = True


class ContractNegotiationAssignment(ContractAssignment):
    """
    Model that links a given contract to a sales employee.
    The employee will be the contact person during negotiation phase
    to sign the contract
    """
    contract = models.OneToOneField(to=Contract, related_name='assigned_contract',
                                    on_delete=models.CASCADE)

    def unique_error_message(self, model_class, unique_check):
        """
        Overridden error message to unique constraint:
        a contract can not be followed by two different employees for the same phase
        """
        if len(unique_check) == 1:
            return ValidationError(
                message=_(f"{self.contract} is already followed"
                          f" by {self.find_assigned_employee_for_contract(self.contract)}"),
                code="unique",
            )
        else:
            return ValidationError(
                message=_(f"{self.contract} is already followed"
                          f" by {self.find_assigned_employee_for_contract(self.contract)}"),
                code="unique_together",
            )

    def clean(self):
        """
        validator: can only be assigned to an employee that is from the sales department
        """
        if not self.employee.is_sales:
            raise ValidationError(
                {NON_FIELD_ERRORS: f'The selected employee {self.employee}'
                                   f' must be a member of the Sales Department'})

    @classmethod
    def find_assigned_employee_for_contract(cls, contract):
        """
        Returns the sales employee who is in charge for the negotiation of a given contract
        """
        return cls.objects.filter(contract=contract).first().employee

    def __str__(self):
        return f'{self.contract} negotiation led by {self.employee}' \
               f' since {self.date_updated}'


class ContractSignatureAssignment(ContractAssignment):
    """
    Model that links a given contract to a sales employee.
    Allows to save the signature details for the contract :
    - signature date
    - employee who is responsible for the signature of the contract
    """
    contract = models.OneToOneField(to=Contract, related_name='signature_contract_status',
                                    on_delete=models.CASCADE)

    def unique_error_message(self, model_class, unique_check):
        """
        Overridden error message to unique constraint:
        a contract can only be signed once
        """
        if len(unique_check) == 1:
            return ValidationError(
                message=_(f"{self.contract} was already signed on {self.contract.date_created}"
                          f" by {self.find_signature_details_for_contract(self.contract)}"),
                code="unique",
            )
        else:
            return ValidationError(
                message=_(f"{self.contract} was already signed on {self.contract.date_created}"
                          f" by {self.find_signature_details_for_contract(self.contract)}"),
                code="unique_together",
            )

    def clean(self):
        """
        validator: the registered employee for signature must be from the sales department
        """
        if not self.employee.is_sales:
            raise ValidationError(
                {NON_FIELD_ERRORS: f'The selected employee {self.employee}'
                                   f' must be a member of the Sales Department'})

    @classmethod
    def find_signature_details_for_contract(cls, contract):
        """
        Returns the sales employee who signed a given contract
        """
        return cls.objects.filter(contract=contract).first().employee

    def __str__(self):
        return f'{self.contract} signature on {self.date_created} by {self.employee}'


class ContractPaymentAssignment(ContractAssignment):
    """
    Model that links a given contract to a sales employee.
    Allows to save the payment details for the contract :
    - payment date
    - employee who is responsible for the payment of the contract
    """
    contract = models.OneToOneField(to=Contract, related_name='payment_contract_status',
                                    on_delete=models.CASCADE)

    def unique_error_message(self, model_class, unique_check):
        """
        Overridden error message to unique constraint:
        a contract can only be registered as paid once
        """
        if len(unique_check) == 1:
            return ValidationError(
                message=_(f"{self.contract} payment was already processed on {self.contract.date_created}"
                          f" by {self.find_payment_details_for_contract(self.contract)}"),
                code="unique",
            )
        else:
            return ValidationError(
                message=_(f"{self.contract} payment was already processed on {self.contract.date_created}"
                          f" by {self.find_payment_details_for_contract(self.contract)}"),
                code="unique_together",
            )

    def clean(self):
        """
        validator: the registered employee for signature must be from the sales department
        """
        if not self.employee.is_sales:
            raise ValidationError(
                {NON_FIELD_ERRORS: f'The selected employee {self.employee}'
                                   f' must be a member of the Sales Department'})

    @classmethod
    def find_payment_details_for_contract(cls, contract):
        """
        Returns the sales employee who registered the payment of a given contract
        """
        return cls.objects.filter(contract=contract).first().employee

    def __str__(self):
        return f'{self.contract} payment on {self.date_created} followed by {self.employee}'


class EventAssignment(Assignment):
    """
    Model that links a given event to a support employee.
    The employee will be the contact person for the event
    """
    event = models.OneToOneField(to=Event, related_name='assigned_event',
                                 on_delete=models.CASCADE)

    def unique_error_message(self, model_class, unique_check):
        """
        Overridden error message to unique constraint:
        an event can only be assigned to one employee from support department
        """
        if len(unique_check) == 1:
            return ValidationError(
                message=_(f"{self.event} is already assigned to"
                          f" {self.find_assigned_employee_for_event(self.event)}"),
                code="unique",
            )
        else:
            return ValidationError(
                message=_(f"{self.event} payment was already processed on to"
                          f" {self.find_assigned_employee_for_event(self.event)}"),
                code="unique_together",
            )

    def clean(self):
        """
        validator: the event can only be assigned to an employee from the support department
        """
        if not self.employee.is_support:
            raise ValidationError(
                {NON_FIELD_ERRORS: f'The selected employee {self.employee}'
                                   f' must be a member of the Support Department'})

    @classmethod
    def find_assigned_employee_for_event(cls, event):
        """
        Returns the support employee who is assigned to a given event
        """
        return cls.objects.filter(event=event).first().employee

    def __str__(self):
        return f'{self.event}  followed by {self.employee}'
