from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


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

    class Meta:
        abstract = True


class Department(Group):

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _("department")
        verbose_name_plural = _("departments")
        db_table = 'departments'
        proxy = True


class Employee(AbstractUser, Person):
    """
    Extends the Basic User class adding some attributes
    the User is renamed "Employee"
    """
    is_staff = models.BooleanField(
        _("staff status"),
        default=True,
        help_text=_("Designates whether the user can log into this admin site."))
    groups = models.ManyToManyField(Department, verbose_name=_("departments"),
                                    help_text=_(
                                        "The department this user belongs to. An Employee will get all custom_permissions "
                                        "granted to  their department."
                                    ),
                                    related_name="user_department",
                                    related_query_name="employee",
                                    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = _('employee')
        verbose_name_plural = _('employees')
