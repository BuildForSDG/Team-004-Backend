# Generated by Django 3.0.6 on 2020-05-25 00:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sme_management', '0006_auto_20200524_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sme',
            name='org_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='smeuser',
            name='sme',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sme_management.SME'),
        ),
    ]
