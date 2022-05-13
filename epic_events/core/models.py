from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from constants import MANAGER, SALES, SUPPORT


class DatedItem(models.Model):
    """
    Abstract parent Class for any dated object
    Returns creation time and last update time
    """
    date_created = models.DateTimeField(_('creation date'), auto_now_add=True)
    date_updated = models.DateTimeField(_('update date'), null=True, auto_now_add=True)

    objects = models.Manager()

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
        """
        Returns the person's first and last name
        """
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
        """
        Returns the department of a given employee
        """
        return self.groups.first() if self.groups.first() else 'Not affected yet'

    @property
    def is_manager(self) -> bool:
        """
        Checks whether the current user is a manager
        """
        return self.department.id == MANAGER

    @property
    def is_sales(self) -> bool:
        """
        Checks whether the current user is from the sales department
        """
        return self.department.id == SALES

    @property
    def is_support(self) -> bool:
        """
        Checks whether the current user is from the support department
        """
        return self.department.id == SUPPORT

    @classmethod
    def set_is_staff(cls, employee_obj):
        """
        Enables a given user to access the administration site
        """
        Employee.objects.filter(pk=employee_obj.id).update(is_staff=True)
        return employee_obj

    def __str__(self):
        return f"{self.get_full_name()} ({self.department})"

    class Meta:
        verbose_name = _('employee')
        verbose_name_plural = _('employees')
