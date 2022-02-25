"""
draft :
- tous les models du projets
- à découper et copier dans les différentes apps quand elles seront créées
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import ForeignKey
from django.utils.translation import gettext_lazy as _


class DatedItem(models.Model):
    date_created = models.DateTimeField(_('creation date'), auto_now_add=True)
    date_updated = models.DateTimeField(_('update date'))  # nullable ?

    class Meta:
        abstract = True


class Person(models.Model):
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
    pass
    # gerer les profils voir django groups !


class Client(Person):
    company_name = models.CharField(_('company name'), max_length=50)
    mobile = models.CharField(_('mobile phone number'), max_length=15)


class Contract(models.Model):
    client = models.ForeignKey(to=Client, related_name='related_client',
                               on_delete=models.CASCADE)  # on delete, à voir... ( passer en AnonymousUser peut etre, cf RGPD)
    sales_person = models.ForeignKey(to=Employee, related_name='related_sales_person',
                                     on_delete=models.CASCADE)  # on delete, à voir... ( passer en AnonymousUser peut etre, cf RGPD)
    signature_date = models.DateField(_('signature date'), null=True, default=None)  #  à verifier ! # sert à rien ! -t> assignation sales employee


class Event(models.Model):
    contract = models.ForeignKey(to=Contract, related_name='retated_contract',
                                 on_delete=models.CASCADE)  # on delete, à voir... ( passer en AnonymousUser peut etre, cf RGPD)
    status = models.CharField(
        _('event status', choices=['created', 'ongoing', 'terminated']))  #  Enum !! voir bon settings
    dates = models.DateField(_('event dates'))


class Assignation(models.Model, DatedItem):
    employee = ForeignKey(to=Employee, related_name='related_employee',
                          on_delete=models.CASCADE)

    class Meta:
        abstract = True


class ClientAssignation(Assignation):
    client = ForeignKey(to=Client, related_name='related_client',
                        on_delete=models.CASCADE)


class ContractAssignation(Assignation):
    contract = ForeignKey(to=Contract, related_name='related_contract',
                          on_delete=models.CASCADE)


class EventAssignation(Assignation):
    event = ForeignKey(to=Event, related_name='related_event',
                       on_delete=models.CASCADE)
