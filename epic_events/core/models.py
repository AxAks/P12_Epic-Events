from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from constants import MANAGER, SALES, SUPPORT


class DatedItem(models.Model):
    """
    Abstract parent Class for any dated object
    """
    date_created = models.DateTimeField(_('creation date'), auto_now_add=True)
    date_updated = models.DateTimeField(_('update date'), null=True, auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'created on {self.date_created}, updated on {self.date_updated}'


class Person(DatedItem):
    """
    Abstract parent class for any physical person representation:
    Can be Employee or Client
    """
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(_('email address'))
    phone = models.CharField(_('phone number'), max_length=15, blank=True)

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        abstract = True


class Employee(AbstractUser, Person):
    """
    Extends the Basic User class adding some attributes
    the User is renamed "Employee"
    """
    groups = models.ManyToManyField(Group, verbose_name=_("department"),
                                    help_text=_(
                                        "The department this user belongs to."
                                        " An Employee will get all custom_permissions "
                                        "granted to  their department."
                                    ),
                                    related_name="user_department",
                                    related_query_name="employee",
                                    )

    @property
    def department(self):
        return self.groups.first() if self.groups.first() else 'Not affected yet'

    def __str__(self):
        return f"{self.get_full_name()} ({self.department})"

    @property
    def is_manager(self) -> bool:
        return self.department.id == MANAGER

    @property
    def is_sales(self) -> bool:
        return self.department.id == SALES

    @property
    def is_support(self) -> bool:
        return self.department.id == SUPPORT

    class Meta:
        verbose_name = _('employee')
        verbose_name_plural = _('employees')
