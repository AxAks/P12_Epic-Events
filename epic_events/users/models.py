from django.db import models
from django.contrib.auth.models import AbstractUser
from abstract.models import DatedItem, Person


class Employee(AbstractUser, Person):
    """
    Extends the Basic User class adding some attributes
    """


class Assignment(DatedItem):
    employee = models.ForeignKey(to=Employee, related_name='related_employee',
                                 on_delete=models.CASCADE)

    class Meta:
        abstract = True
