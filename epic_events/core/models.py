from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class DatedItem(models.Model):
    date_created = models.DateTimeField(_('creation date'), auto_now_add=True)
    date_updated = models.DateTimeField(_('update date'), null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'created on {self.date_created}, updated on {self.date_updated}'


class Person(DatedItem):
    """

    """
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
    the User is renamed "Employee"
    """

    class Meta:
        verbose_name = _('employee')
        verbose_name_plural = _('employees')


class Profile(models.Model):
    MANAGER = 1
    SALES = 2
    SUPPORT = 3
    USERS_ROLES = (
        (MANAGER, 'Manager'),
        (SALES, 'Sales'),
        (SUPPORT, 'Support'),
    )

    employee = models.ForeignKey(to=Employee, related_name='employee_profile',
                                 on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField(_('role'), choices=USERS_ROLES,
                                            null=True, blank=True)

    def __str__(self):
        return f'{self.employee.last_name}, {self.employee.first_name}'


@receiver(post_save, sender=Employee)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(employee=instance)
    instance.profile.save()
