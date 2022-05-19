from django_filters import FilterSet

from api.models import Event, Contract
from core.models import DatedItem


class DatedItemFilter(FilterSet):
    """
    Class to be used to sort dated Objects by creation or update date
    """

    class Meta:
        model = DatedItem
        fields = {
            'date_created': ['lt', 'gte'],
            'date_updated': ['lt', 'gte']
        }


class ContractFilter(DatedItemFilter):
    """
    Class to be used to sort dated Objects by creation or update date
    """

    class Meta:

        model = Contract
        fields = {
            'id': 'exact',
            'client__last_name': 'exact',
            'client__email': 'exact',
            'amount_in_cts': 'exact',
            'date_created': ['lt', 'gte'],
            'date_updated': ['lt', 'gte']
        }


class EventDatesFilter(FilterSet):
    """
    Class for custom Event filter by start and end date of the Event
    """

    class Meta:
        model = Event
        fields = {
            'begin_date': ['lt', 'gte'],
            'end_date': ['lt', 'gte']
        }
