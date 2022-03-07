"""
draft :
- tous les models du projets
- à découper et copier dans les différentes apps quand elles seront créées ?si je fais des apps, utile ?
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from constants import STATUSES
from epic_events.users.models import Client, Employee


class Contract(DatedItem):
    client = models.ForeignKey(to=Client, related_name='related_client',
                               on_delete=models.CASCADE)  # on delete, à voir... ( passer en AnonymousUser peut etre, cf RGPD)
    sales_person = models.ForeignKey(to=Employee, related_name='related_sales_person',
                                     on_delete=models.CASCADE)  # on delete, à voir... ( passer en AnonymousUser peut etre, cf RGPD)


class Event(DatedItem):
    contract = models.ForeignKey(to=Contract, related_name='related_contract',
                                 on_delete=models.CASCADE)  # on delete, à voir... ( passer en AnonymousUser peut etre, cf RGPD)
    status = models.CharField(
        _('event status', choices=STATUSES))  #  Enum !! voir bon settings
    begin_date = models.DateField(_('begin date'))
    end_date = models.DateField(_('end date'))


class Assignment(DatedItem):
    employee = models.ForeignKey(to=Employee, related_name='related_employee',
                                 on_delete=models.CASCADE)

    class Meta:
        abstract = True


class ClientAssignment(Assignment):
    client = models.ForeignKey(to=Client, related_name='related_client',
                               on_delete=models.CASCADE)


class ContractAssignment(Assignment):
    contract = models.ForeignKey(to=Contract, related_name='related_contract',
                                 on_delete=models.CASCADE)


class EventAssignment(Assignment):
    event = models.ForeignKey(to=Event, related_name='related_event',
                              on_delete=models.CASCADE)
