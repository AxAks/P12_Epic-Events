from rest_framework import serializers, validators

from api.models import Client, Contract, Event, ClientAssignment, \
    ContractNegotiationAssignment, ContractSignatureAssignment, EventAssignment, ContractPaymentAssignment
from core.models import Employee


class ClientSerializer(serializers.ModelSerializer):
    """
    Serializer for Clients
    """
    class Meta:
        model = Client
        fields = ('id', 'first_name', 'last_name', 'email',
                  'phone', 'company_name', 'mobile',
                  'date_created', 'date_updated')
        read_only_fields = ('date_created', 'date_updated')


class ContractSerializer(serializers.ModelSerializer):
    """
    Serializer for Contracts
    """
    class Meta:
        model = Contract
        fields = ('id', 'client', 'amount_in_cts', 'due_date',
                  'date_created', 'date_updated')
        read_only_fields = ('due_date', 'date_created', 'date_updated')

    def save(self) -> Contract:
        contract = Contract(
            client=self.validated_data['client'],
            amount_in_cts=self.validated_data['amount_in_cts'],
        )
        client = Client.objects.filter(id=contract.client.id).first()

        errors = {}
        if not client.is_assigned:
            errors['client_must_be_assigned'] = f'The selected client {contract.client}' \
                                                f' must be assigned to a sales employee first'

        if errors:
            raise serializers.ValidationError(errors)

        contract.save()
        return contract


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for Event
    """
    class Meta:
        model = Event
        fields = ('id', 'name', 'contract', 'status',
                  'begin_date', 'end_date', 'attendees', 'notes',
                  'date_created', 'date_updated')
        read_only_fields = ('date_created', 'date_updated')

    def save(self) -> Event:
        event = Event(
            name=self.validated_data['name'],
            contract=self.validated_data['contract'],
            status=self.validated_data['status'],
            begin_date=self.validated_data['begin_date'],
            end_date=self.validated_data['end_date'],
            attendees=self.validated_data['attendees'],
            notes=self.validated_data['notes'],
        )
        contract = Contract.objects.filter(id=event.contract.id).first()

        errors = {}
        if not contract.is_signed:
            errors['must_be_signed'] = f'The related contract: {event.contract}' \
                                               f' must be signed before the event can be created'

        if errors:
            raise serializers.ValidationError(errors)

        event.save()
        return event


class AssignmentSerializer(serializers.ModelSerializer):
    """
    Abstract parent class for Assignment Serializers
    """
    exclude = ('date_created', 'date_updated')
    read_only_fields = ('date_created', 'date_updated')

    class Meta:
        abstract = True


class ClientAssignmentSerializer(AssignmentSerializer):
    """
    Serializer for client follow-up assignment
    """
    class Meta:
        model = ClientAssignment
        fields = ('id', 'employee', 'client', 'date_created', 'date_updated')
        read_only_fields = ('date_created', 'date_updated')

    def __init__(self, *args, **kwargs):
        """
        Overrides parent init to add business logic
        and return custom error messages
        """
        super(ClientAssignmentSerializer, self).__init__(*args, **kwargs)
        for validator in self.fields['client'].validators:
            if isinstance(validator, validators.UniqueValidator):
                validator.message = 'This client is already followed by an employee'

    def save(self) -> ClientAssignment:
        client_assignment = ClientAssignment(
            employee=self.validated_data['employee'],
            client=self.validated_data['client'],
        )

        errors = {}
        selected_employee = Employee.objects.filter(id=client_assignment.employee.id).first()

        if not selected_employee.is_sales:
            errors['must_be_sales_employee'] = f'The selected employee {client_assignment.employee}' \
                                               f' must be a member of the Sales Department'

        if errors:
            raise serializers.ValidationError(errors)

        client_assignment.save()
        return client_assignment


class ContractNegotiationAssignmentSerializer(AssignmentSerializer):
    """
    Serializer for contract negotiation follow-up assignment
    """
    class Meta:
        model = ContractNegotiationAssignment
        fields = ('id', 'employee', 'contract', 'date_created', 'date_updated')
        read_only_fields = ('date_created', 'date_updated')

    def __init__(self, *args, **kwargs):
        """
        Overrides parent init to add business logic
        and return custom error messages
        """
        super(ContractNegotiationAssignmentSerializer, self).__init__(*args, **kwargs)
        for validator in self.fields['contract'].validators:
            if isinstance(validator, validators.UniqueValidator):
                validator.message = 'This contract is already followed by an employee'

    def save(self) -> ContractNegotiationAssignment:
        contract_negotiation_assignment = ContractNegotiationAssignment(
            employee=self.validated_data['employee'],
            contract=self.validated_data['contract'],
        )

        errors = {}
        employee = Employee.objects.filter(id=contract_negotiation_assignment.employee.id).first()

        if not employee.is_sales:
            errors['must_be_sales_employee'] = f'The selected employee {contract_negotiation_assignment.employee}' \
                                                 f' must be a member of the Sales Department'
        if errors:
            raise serializers.ValidationError(errors)

        contract_negotiation_assignment.save()
        return contract_negotiation_assignment


class ContractSignatureAssignmentSerializer(AssignmentSerializer):
    """
    Serializer for contract signature details registration
    """
    class Meta:
        model = ContractSignatureAssignment
        fields = ('id', 'employee', 'contract', 'date_created', 'date_updated')
        read_only_fields = ('date_created', 'date_updated')

    def __init__(self, *args, **kwargs):
        """
        Overrides parent init to add business logic
        and return custom error messages
        """
        super(ContractSignatureAssignmentSerializer, self).__init__(*args, **kwargs)
        for validator in self.fields['contract'].validators:
            if isinstance(validator, validators.UniqueValidator):
                validator.message = 'This contract has already been signed'

    def save(self) -> ContractSignatureAssignment:
        contract_signature_assignment = ContractSignatureAssignment(
            employee=self.validated_data['employee'],
            contract=self.validated_data['contract'],
        )

        errors = {}
        employee = Employee.objects.filter(id=contract_signature_assignment.employee.id).first()
        contract = Contract.objects.filter(id=contract_signature_assignment.contract.id).first()

        if not employee.is_sales:
            errors['must_be_sales_employee'] = f'The selected employee {contract_signature_assignment.employee}'\
                                                 f' must be a member of the Sales Department'
        if not contract.registered_negotiator:
            errors['no_negotiator_registered'] = f'The negotiation for :' \
                                                 f' {contract_signature_assignment.contract}'\
                                                 f' must be registered before it can be signed'

        if errors:
            raise serializers.ValidationError(errors)

        contract_signature_assignment.save()
        return contract_signature_assignment


class ContractPaymentAssignmentSerializer(AssignmentSerializer):
    """
    Serializer for contract payment details registration
    """
    class Meta:
        model = ContractPaymentAssignment
        fields = ('id', 'employee', 'contract', 'date_created', 'date_updated')
        read_only_fields = ('date_created', 'date_updated')

    def __init__(self, *args, **kwargs):
        """
        Overrides parent init to add business logic
        and return custom error messages
        """
        super(ContractPaymentAssignmentSerializer, self).__init__(*args, **kwargs)
        for validator in self.fields['contract'].validators:
            if isinstance(validator, validators.UniqueValidator):
                validator.message = 'This contract has already been signed'

    def save(self) -> ContractPaymentAssignment:
        contract_payment_assignment = ContractPaymentAssignment(
            employee=self.validated_data['employee'],
            contract=self.validated_data['contract'],
        )

        errors = {}
        employee = Employee.objects.filter(id=contract_payment_assignment.employee.id).first()
        is_signed = contract_payment_assignment.contract.is_signed

        if not employee.is_sales:
            errors['must_be_sales_employee'] = f'The selected employee {contract_payment_assignment.employee}' \
                                               f' ({contract_payment_assignment.employee.groups.first()})' \
                                                 f' is not a member of the Sales Department'
        if not is_signed:
            errors['contract_not_signed'] = f'The contract {contract_payment_assignment.contract}' \
                                            f'has to be signed before being paid'
        if errors:
            raise serializers.ValidationError(errors)

        contract_payment_assignment.save()
        return contract_payment_assignment


class EventAssignmentSerializer(AssignmentSerializer):
    """
    Serializer for Events
    """
    class Meta:
        model = EventAssignment
        fields = ('id', 'employee', 'event', 'date_created', 'date_updated')
        read_only_fields = ('date_created', 'date_updated')

    def __init__(self, *args, **kwargs):
        """
        Overrides parent init to add business logic
        and return custom error messages
        """
        super(EventAssignmentSerializer, self).__init__(*args, **kwargs)
        for validator in self.fields['event'].validators:
            if isinstance(validator, validators.UniqueValidator):
                validator.message = 'This event is already assigned to an employee'

    def save(self) -> EventAssignment:
        event_assignment = EventAssignment(
            employee=self.validated_data['employee'],
            event=self.validated_data['event'],
        )

        errors = {}
        employee = Employee.objects.filter(id=event_assignment.employee.id).first()

        if not employee.is_support:
            errors['must_be_support_employee'] = f'The selected employee {event_assignment.employee}' \
                                                 f' must be a member of the Support Department'

        if errors:
            raise serializers.ValidationError(errors)

        event_assignment.save()
        return event_assignment
