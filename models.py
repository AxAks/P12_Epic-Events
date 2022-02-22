"""
draft :
- tous les models du projets
- à découper et copier dans les différentes apps quand elles seront créées
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    Extends the Basic User class adding some attributes
    """
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(_('email address'))
    phone = models.IntegerField(_('phone number')) # pas integer, voir si formal tel existe
    profile = models.CharField(_('profile', choices=['Manager', 'Salesperson', 'Assignee'])) # Enum !! voir bon settings
    date_created = models.DateTimeField(_('creation date'), auto_now_add=True)
    date_updated = models.DateTimeField(_('update date'))

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Contact:
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(_('email address'))
    phone = models.IntegerField(_('phone number')) # pas integer, voir si formal tel existe
    mobile = models.IntegerField(_('mobile phone number')) # pas integer, voir si formal tel existe
    company_name = models.CharField(_('company name'))
    is_client = models.BooleanField(_('is the contact already a client'))
    date_created = models.DateTimeField(_('creation date'), auto_now_add=True)
    date_updated = models.DateTimeField(_('update date'))

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Contract:
    client = models.ForeignKey(to=Contact, related_name='related_client',
                               on_delete=models.CASCADE) # on delete, à voir... ( passer en AnonymousUser peut etre, cf RGPD)
    salesperson = models.ForeignKey(to=CustomUser, related_name='related_salesperson',
                                    on_delete=models.CASCADE) # on delete, à voir... ( passer en AnonymousUser peut etre, cf RGPD)
    status = models.CharField(_('contract status', choices=['created', 'ongoing', 'signed'])) # Enum !! voir bon settings ( passer la liste en constante ?
    attribution_date = models.DateField(_('attribution date'))
    signature_date = models.DateField(_('signature date'))
    date_created = models.DateTimeField(_('creation date'), auto_now_add=True)
    date_updated = models.DateTimeField(_('update date'))


class Event:
    contract = models.ForeignKey(to=Contract, related_name='retated_contract',
                                 on_delete=models.CASCADE) # on delete, à voir... ( passer en AnonymousUser peut etre, cf RGPD)
    representative = models.ForeignKey(to=CustomUser, related_name='assignee',
                                       on_delete=models.CASCADE)  # on delete, à voir... ( passer en AnonymousUser peut etre, cf RGPD)
    status = models.CharField(_('event status', choices=['created', 'ongoing', 'terminated']))  #  Enum !! voir bon settings
    attribution_date = models.DateField(_('attribution date'))  # date ou datetime à voir + auto
    dates = models.DateField(_('event dates'))
    date_created = models.DateTimeField(_('creation date'), auto_now_add=True)
    date_updated = models.DateTimeField(_('update date'))

