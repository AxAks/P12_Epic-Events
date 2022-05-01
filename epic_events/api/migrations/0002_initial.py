# Generated by Django 4.0.3 on 2022-05-01 16:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventassignment',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='eventassignment',
            name='event',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_event', to='api.event'),
        ),
        migrations.AddField(
            model_name='event',
            name='contract',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='event_contract', to='api.contract'),
        ),
        migrations.AddField(
            model_name='contractsignatureassignment',
            name='contract',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='signature_contract_status', to='api.contract'),
        ),
        migrations.AddField(
            model_name='contractsignatureassignment',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contractpaymentassignment',
            name='contract',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment_contract_status', to='api.contract'),
        ),
        migrations.AddField(
            model_name='contractpaymentassignment',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contractnegotiationassignment',
            name='contract',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_contract', to='api.contract'),
        ),
        migrations.AddField(
            model_name='contractnegotiationassignment',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contract',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contractor', to='api.client'),
        ),
        migrations.AddField(
            model_name='clientassignment',
            name='client',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_client', to='api.client'),
        ),
        migrations.AddField(
            model_name='clientassignment',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
