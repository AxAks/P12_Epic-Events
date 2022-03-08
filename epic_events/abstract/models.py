from django.db import models
from django.utils.translation import gettext_lazy as _


class DatedItem(models.Model):
    date_created = models.DateTimeField(_('creation date'), auto_now_add=True)
    date_updated = models.DateTimeField(_('update date'), null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'created on {self.date_created}, updated on {self.date_updated}'


class Person(DatedItem):
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(_('email address'))
    phone = models.CharField(_('phone number'), max_length=15)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
