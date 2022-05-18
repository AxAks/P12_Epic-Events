from django_filters import FilterSet

from api.models import Event
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
