"""
draft :
- tous les models du projets
- à découper et copier dans les différentes apps quand elles seront créées ?si je fais des apps, utile ?
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from constants import STATUSES


class DatedItem(models.Model):
    date_created = models.DateTimeField(_('creation date'), auto_now_add=True)
    date_updated = models.DateTimeField(_('update date', nullable=True, Default=None))

    class Meta:
        abstract = True


class Person(DatedItem):
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(_('email address'))
    phone = models.CharField(_('phone number'), max_length=15)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Employee(AbstractUser, Person):
    """
    Extends the Basic User class adding some attributes
    """
    pass  # gerer les profils voir django groups !


class Client(Person):
    company_name = models.CharField(_('company name'), max_length=50)
    mobile = models.CharField(_('mobile phone number'), max_length=15)


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
