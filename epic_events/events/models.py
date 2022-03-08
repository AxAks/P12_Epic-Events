from django.db import models
from django.utils.translation import gettext_lazy as _
from constants import STATUSES
from abstract.models import DatedItem
from users.models import Assignment
from contracts.models import Contract


class Event(DatedItem):
    contract = models.ForeignKey(to=Contract, related_name='event_contract',
                                 on_delete=models.CASCADE)  # on delete, à voir... ( passer en AnonymousUser peut etre, cf RGPD)
    status = models.CharField(max_length=10, choices=STATUSES)  #  Enum !! voir bon settings
    begin_date = models.DateField(_('begin date'))
    end_date = models.DateField(_('end date'))


class EventAssignment(Assignment):
    event = models.ForeignKey(to=Event, related_name='assigned_event',
                              on_delete=models.CASCADE)
