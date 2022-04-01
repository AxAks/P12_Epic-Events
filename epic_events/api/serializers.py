from rest_framework import serializers

from api.models import Client, Contract, Event, ClientAssignment, ContractAssignment, EventAssignment
from constants import SUPPORT, SALES


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'company_name', 'mobile')


class ContractSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contract
        fields = ('id', 'client', 'sales_person', 'status', 'amount_in_cts', 'due_date')


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'name', 'contract', 'status', 'begin_date', 'end_date', 'attendees', 'notes')


class ClientAssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientAssignment
        fields = ('id', 'employee', 'client')

    def save(self) -> ClientAssignment:
        client_assignment = ClientAssignment(
            employee=self.validated_data['employee'],
            client=self.validated_data['client'],
        )
        is_sales_employee = client_assignment.employee.groups.first().id == SALES \
            if client_assignment.employee.groups.first() else False
        already_assigned = [ClientAssignment.objects.filter(employee=client_assignment.employee).first()]

        errors = {}
        if not is_sales_employee:
            errors['must_be_sales_employee'] = f'The selected employee {client_assignment.employee}' \
                                               f' ({client_assignment.employee.groups.first()})' \
                                               f' is not a member of the Sales Department'
        if already_assigned:
            errors['already_assigned_client'] = f'The client {client_assignment.client} is already assigned ' \
                                                f'to {client_assignment.employee}' \
                                                f'  ({client_assignment.employee.groups.first()})'
        if errors:
            raise serializers.ValidationError(errors)

        client_assignment.save()
        return client_assignment


class ContractAssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContractAssignment
        fields = ('id', 'employee', 'contract')

    def save(self) -> ContractAssignment:
        contract_assignment = ContractAssignment(
            employee=self.validated_data['employee'],
            contract=self.validated_data['contract'],
        )
        is_sales_employee = contract_assignment.employee.groups.first().id == SALES \
            if contract_assignment.employee.groups.first() else False
        already_assigned = [ContractAssignment.objects.filter(employee=contract_assignment.employee).first()]

        errors = {}
        if not is_sales_employee:
            errors['must_be_sales_employee'] = f'The selected employee {contract_assignment.employee}' \
                                               f' ({contract_assignment.employee.groups.first()})' \
                                                 f' is not a member of the Sales Department'

        if already_assigned:
            errors['already_assigned_client'] = f'The contract {contract_assignment.contract}' \
                                                f' is already assigned to {contract_assignment.employee}' \
                                                f' ({contract_assignment.employee.groups.first()})'

        if errors:
            raise serializers.ValidationError(errors)

        contract_assignment.save()
        return contract_assignment


class EventAssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventAssignment
        fields = ('id', 'employee', 'event')

    def save(self) -> EventAssignment:
        event_assignment = EventAssignment(
            employee=self.validated_data['employee'],
            event=self.validated_data['event'],
        )
        is_support_employee = event_assignment.employee.groups.first().id == SUPPORT \
            if event_assignment.employee.groups.first() else False
        already_assigned = [ContractAssignment.objects.filter(employee=event_assignment.employee).first()]

        errors = {}
        if not is_support_employee:
            errors['must_be_support_employee'] = f'The selected employee {event_assignment.employee}' \
                                                 f' is not a member of the Support Department'
        if already_assigned:
            errors['already_assigned_client'] = f'The event {event_assignment.event}' \
                                                f' is already assigned to {event_assignment.employee}' \
                                                f' ({event_assignment.employee.groups.first()})'

        if errors:
            raise serializers.ValidationError(errors)

        event_assignment.save()
        return event_assignment
