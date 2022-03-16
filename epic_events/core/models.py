from django.db import models
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from constants import USERS_ROLES


class DatedItem(models.Model):
    """
    Abstract parent Class for any dated object
    """
    date_created = models.DateTimeField(_('creation date'), auto_now_add=True)
    date_updated = models.DateTimeField(_('update date'), null=True)

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


class Employee(AbstractUser, Person):
    """
    Extends the Basic User class adding some attributes
    the User is renamed "Employee"
    """
    is_staff = models.BooleanField(
        _("staff status"),
        default=True,
        help_text=_("Designates whether the user can log into this admin site."))

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = _('employee')
        verbose_name_plural = _('employees')


class Department(Group):

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _("department")
        verbose_name_plural = _("departments")
        proxy = True
        app_label = 'auth'


class Affiliation(DatedItem):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    department = models.OneToOneField(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.employee} ({self.department})'

# class Profile(models.Model):
#     """
#     Defines employees roles
#     """
#     employee = models.OneToOneField(to=Employee, related_name='profile',
#                                     on_delete=models.CASCADE)
#     role = models.PositiveSmallIntegerField(_('role'), choices=USERS_ROLES,
#                                             default=3)
#
#     def __str__(self):
#         return f'{USERS_ROLES[self.role - 1][1]}'
#
#
# @receiver(post_save, sender=Employee)
# def create_or_update_employee_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(employee=instance)
#     instance.profile.save()
