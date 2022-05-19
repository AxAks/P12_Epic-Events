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
        fields = ['id', 'client__last_name', 'client__email', 'amount_in_cts']


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

"""
def get_contracts_filterset_class(request):
    params = {param for param in request.query_params}
    if not params.keys()
    elif 'date_created_gte' or 'date_created_lt' or 'date_updated_gte' or 'date_updated_lt' in params.keys()
        return DatedItemFilter
    elif 'id' or 'client__last_name' or 'client__email' or 'amount_in_cts' in params.keys()
        return ContractFilter
"""