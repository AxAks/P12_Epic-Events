from rest_framework import serializers

from api.models import Client, Contract, Event


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
