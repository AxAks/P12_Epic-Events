from django.db import models
from django.utils.translation import gettext_lazy as _
from abstract.models import Person, DatedItem
from users.models import Employee, Assignment


class Client(Person):
    company_name = models.CharField(_('company name'), max_length=50)
    mobile = models.CharField(_('mobile phone number'), max_length=15)


class Contract(DatedItem):
    client = models.ForeignKey(to=Client, related_name='related_client',
                               on_delete=models.CASCADE)  # on delete, à voir... ( passer en AnonymousUser peut etre, cf RGPD)
    sales_person = models.ForeignKey(to=Employee, related_name='related_sales_person',
                                     on_delete=models.CASCADE)  # on delete, à voir... ( passer en AnonymousUser peut etre, cf RGPD)


class ClientAssignment(Assignment):
    client = models.ForeignKey(to=Client, related_name='related_client',
                               on_delete=models.CASCADE)


class ContractAssignment(Assignment): # pourquoi ??
    contract = models.ForeignKey(to=Contract, related_name='related_contract',
                                 on_delete=models.CASCADE)