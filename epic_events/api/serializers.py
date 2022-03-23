from rest_framework import serializers

from api.models import Client


class ClientSerializer(serializers.ModelSerializer):
    pass

    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'email', 'phone', 'company_name', 'mobile')
