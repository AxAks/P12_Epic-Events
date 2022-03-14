# Generated by Django 4.0.3 on 2022-03-12 00:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='amount_in_cts',
            field=models.IntegerField(default=0, verbose_name='amount'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contract',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 12, 0, 3, 53, 665041), verbose_name='due_date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contract',
            name='status',
            field=models.BooleanField(default=False, verbose_name='status'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='attendees',
            field=models.IntegerField(default=0, verbose_name='attendees'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='notes',
            field=models.TextField(default='', verbose_name='notes'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='begin_date',
            field=models.DateTimeField(verbose_name='begin date'),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateTimeField(verbose_name='end date'),
        ),
    ]