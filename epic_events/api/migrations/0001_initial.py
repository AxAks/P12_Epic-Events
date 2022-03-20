# Generated by Django 4.0.3 on 2022-03-20 01:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('date_updated', models.DateTimeField(auto_now_add=True, null=True, verbose_name='update date')),
                ('first_name', models.CharField(max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(max_length=150, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, verbose_name='email address')),
                ('phone', models.CharField(blank=True, max_length=15, verbose_name='phone number')),
                ('company_name', models.CharField(max_length=50, verbose_name='company name')),
                ('mobile', models.CharField(max_length=15, verbose_name='mobile phone number')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ClientAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('date_updated', models.DateTimeField(auto_now_add=True, null=True, verbose_name='update date')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('date_updated', models.DateTimeField(auto_now_add=True, null=True, verbose_name='update date')),
                ('status', models.BooleanField(verbose_name='status')),
                ('amount_in_cts', models.IntegerField(verbose_name='amount')),
                ('due_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='due_date')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContractAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('date_updated', models.DateTimeField(auto_now_add=True, null=True, verbose_name='update date')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('date_updated', models.DateTimeField(auto_now_add=True, null=True, verbose_name='update date')),
                ('status', models.IntegerField(choices=[(1, 'created'), (2, 'ongoing'), (3, 'terminated')])),
                ('begin_date', models.DateTimeField(verbose_name='begin date')),
                ('end_date', models.DateTimeField(verbose_name='end date')),
                ('attendees', models.IntegerField(default=0, verbose_name='attendees')),
                ('notes', models.TextField(verbose_name='notes')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EventAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('date_updated', models.DateTimeField(auto_now_add=True, null=True, verbose_name='update date')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
