from django_filters import FilterSet

from api.models import Event, Contract, ClientAssignment, ContractNegotiationAssignment, ContractSignatureAssignment, \
    ContractPaymentAssignment, EventAssignment
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
        dated_item_filters = {field: lookup for (field, lookup) in DatedItemFilter.Meta.fields.items()}
        for field, lookup in dated_item_filters.items():
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

        fields = {'id': ['exact'],
                  'contract__client__last_name': ['exact'],
                  'contract__client__email': ['exact'],
                  'begin_date': ['lt', 'gte'],
                  'end_date': ['lt', 'gte']
                  }


class ClientAssignmentFilter(DatedItemFilter):
    """
    Class to filter Client assignments
    """

    class Meta:
        model = ClientAssignment
        current_filters = {'id': ['exact'],
                           'client__last_name': ['exact'],
                           'client__email': ['exact'],
                           'employee__last_name': ['exact'],
                           'employee__email': ['exact'],
                           }
        fields = DatedItemFilter.combined_dated_item_filters_and_current_filters(current_filters)


class ContractNegotiationAssignmentFilter(DatedItemFilter):
    """
    Class to filter Contract assignments for negotiation
    """

    class Meta:
        model = ContractNegotiationAssignment
        current_filters = {'id': ['exact'],
                           'contract__client__last_name': ['exact'],
                           'contract__client__email': ['exact'],
                           'employee__last_name': ['exact'],
                           'employee__email': ['exact']
                           }
        fields = DatedItemFilter.combined_dated_item_filters_and_current_filters(current_filters)


class ContractSignatureAssignmentFilter(DatedItemFilter):
    """
    Class to filter Contract signature details
    """

    class Meta:
        model = ContractSignatureAssignment
        current_filters = {'id': ['exact'],
                           'contract__client__last_name': ['exact'],
                           'contract__client__email': ['exact'],
                           'employee__last_name': ['exact'],
                           'employee__email': ['exact']
                           }
        fields = DatedItemFilter.combined_dated_item_filters_and_current_filters(current_filters)


class ContractPaymentAssignmentFilter(DatedItemFilter):
    """
    Class to filter Contract payment details
    """

    class Meta:
        model = ContractPaymentAssignment
        current_filters = {'id': ['exact'],
                           'contract__client__last_name': ['exact'],
                           'contract__client__email': ['exact'],
                           'employee__last_name': ['exact'],
                           'employee__email': ['exact']
                           }
        fields = DatedItemFilter.combined_dated_item_filters_and_current_filters(current_filters)


class EventAssignmentFilter(DatedItemFilter):
    """
    Class to filter Event Assignments
    """

    class Meta:
        model = EventAssignment
        current_filters = {'id': ['exact'],
                           'event__contract__client__last_name': ['exact'],
                           'event__contract__client__email': ['exact'],
                           'employee__last_name': ['exact'],
                           'employee__email': ['exact']
                           }
        fields = DatedItemFilter.combined_dated_item_filters_and_current_filters(current_filters)
