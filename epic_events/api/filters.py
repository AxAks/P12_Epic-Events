from django_filters import FilterSet

from api.models import Event, Contract
from core.models import DatedItem


class DatedItemFilter(FilterSet):
    """
    Class to be used to sort dated Objects by creation or update date
    """
    @classmethod
    def combined_dated_item_filters_and_current_filters(cls, current_filters) -> dict:
        """
        enables to add date filters to a class filter derived from DatedItem
        """
        dated_item_filters = {field: lookup for (field, lookup) in DatedItemFilter.meta.fields.items()}
        for field, lookup  in dated_item_filters.items():
            current_filters[field] = lookup
        dated_models_combined_filters = current_filters
        return dated_models_combined_filters

    class Meta:
        model = DatedItem
        fields = {
            'date_created': ['lt', 'gte'],
            'date_updated': ['lt', 'gte']
        }


class ContractFilter(DatedItemFilter):
    """
    Class to be used to sort Contracts
    """

    class Meta:
        model = Contract
        current_filters = {'id': ['exact'],
                           'client__last_name': ['exact'],
                           'client__email': ['exact'],
                           'amount_in_cts': ['exact']}
        fields = DatedItemFilter.combined_dated_item_filters_and_current_filters(current_filters)


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
